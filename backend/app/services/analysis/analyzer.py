from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.data_source import DataSource
from app.models.alert import Alert, AlertMetadata
from app.models.soda_report import SoDAReport, SoDAReportMetadata
from app.models.finding import Finding
from app.models.analysis_run import AnalysisRun
from app.models.issue_group import IssueGroup
from app.models.focus_area import FocusArea

from .classifier import FocusAreaClassifier, IssueTypeClassifier
from .risk_scorer import RiskScorer


class Analyzer:
    """Main analysis engine that processes data sources and creates findings"""
    
    def __init__(self, db: Session):
        self.db = db
        self.focus_classifier = FocusAreaClassifier(db)
        self.issue_classifier = IssueTypeClassifier(db)
        self.risk_scorer = RiskScorer()
    
    def analyze_data_source(self, data_source_id: int) -> AnalysisRun:
        """
        Analyze a data source and create findings
        
        Returns:
            AnalysisRun with results
        """
        # Get data source
        data_source = self.db.query(DataSource).filter(
            DataSource.id == data_source_id
        ).first()
        
        if not data_source:
            raise ValueError(f"Data source {data_source_id} not found")
        
        # Create analysis run
        analysis_run = AnalysisRun(
            run_name=f"Analysis of {data_source.filename}",
            status="running",
            started_at=datetime.utcnow()
        )
        self.db.add(analysis_run)
        self.db.commit()
        
        try:
            findings = []
            
            # Process based on data type
            if data_source.data_type.value == "alert":
                findings = self._analyze_alert(data_source, analysis_run)
            elif data_source.data_type.value == "report":
                findings = self._analyze_report(data_source, analysis_run)
            
            # Group findings by issue type
            self._group_findings(findings, analysis_run)
            
            # Update analysis run
            analysis_run.status = "completed"
            analysis_run.completed_at = datetime.utcnow()
            analysis_run.total_findings = len(findings)
            
            # Calculate summary statistics
            findings_by_focus = {}
            findings_by_issue = {}
            total_risk = 0
            total_money_loss = 0.0
            
            for finding in findings:
                # By focus area
                fa_code = finding.focus_area.code
                findings_by_focus[fa_code] = findings_by_focus.get(fa_code, 0) + 1
                
                # By issue type
                if finding.issue_type:
                    it_code = finding.issue_type.code
                    findings_by_issue[it_code] = findings_by_issue.get(it_code, 0) + 1
                
                # Risk and money loss
                if finding.risk_assessment:
                    total_risk += finding.risk_assessment.risk_score
                if finding.money_loss_calculation:
                    total_money_loss += finding.money_loss_calculation.estimated_loss
            
            analysis_run.findings_by_focus_area = findings_by_focus
            analysis_run.findings_by_issue_type = findings_by_issue
            analysis_run.total_risk_score = total_risk
            analysis_run.total_money_loss = total_money_loss
            
            self.db.commit()
            
        except Exception as e:
            analysis_run.status = "failed"
            analysis_run.error_message = str(e)
            self.db.commit()
            raise
        
        return analysis_run
    
    def _analyze_alert(self, data_source: DataSource, analysis_run: AnalysisRun) -> List[Finding]:
        """Analyze 4C alert data source"""
        findings = []
        
        # Get alert metadata
        alert_metadata = self.db.query(AlertMetadata).filter(
            AlertMetadata.data_source_id == data_source.id
        ).first()
        
        if not alert_metadata:
            return findings
        
        # Get alerts
        alerts = self.db.query(Alert).filter(
            Alert.data_source_id == data_source.id
        ).all()
        
        # Classify focus area
        focus_area, focus_confidence = self.focus_classifier.classify(
            alert_name=alert_metadata.alert_name,
            data={"alert_id": alert_metadata.alert_id}
        )
        
        if not focus_area:
            return findings
        
        # Classify issue type
        issue_type, issue_confidence = self.issue_classifier.classify(
            focus_area=focus_area,
            alert_name=alert_metadata.alert_name,
            data={"alert_id": alert_metadata.alert_id}
        )
        
        # Create finding for each alert (or aggregate)
        # For now, create one finding per alert
        for alert in alerts:
            finding = Finding(
                data_source_id=data_source.id,
                alert_id=alert.id,
                focus_area_id=focus_area.id,
                issue_type_id=issue_type.id if issue_type else None,
                title=f"{alert_metadata.alert_name} - {alert.user_name or 'Unknown User'}",
                description=f"Alert detected: {alert_metadata.alert_name}",
                severity=issue_type.default_severity if issue_type else "Medium",
                classification_confidence=min(focus_confidence, issue_confidence) if issue_type else focus_confidence,
                detected_at=alert.timestamp or alert.created_at
            )
            self.db.add(finding)
            self.db.flush()
            
            # Calculate risk assessment
            risk_data = self.risk_scorer.calculate_risk_score(finding, issue_type)
            from app.models.risk_assessment import RiskAssessment
            risk_assessment = RiskAssessment(
                finding_id=finding.id,
                **risk_data,
                risk_description=f"Risk associated with {alert_metadata.alert_name}",
                affected_users=1
            )
            self.db.add(risk_assessment)
            
            findings.append(finding)
        
        return findings
    
    def _analyze_report(self, data_source: DataSource, analysis_run: AnalysisRun) -> List[Finding]:
        """Analyze SoDA report data source"""
        findings = []
        
        # Get report metadata
        report_metadata = self.db.query(SoDAReportMetadata).filter(
            SoDAReportMetadata.data_source_id == data_source.id
        ).first()
        
        if not report_metadata:
            return findings
        
        # Get reports
        reports = self.db.query(SoDAReport).filter(
            SoDAReport.data_source_id == data_source.id
        ).all()
        
        # Classify focus area (SoDA reports are typically Access Governance)
        focus_area, focus_confidence = self.focus_classifier.classify(
            report_type=report_metadata.report_type,
            data={"report_type": report_metadata.report_type}
        )
        
        # Default to Access Governance if not classified
        if not focus_area:
            focus_area = self.db.query(FocusArea).filter(
                FocusArea.code == "ACCESS_GOVERNANCE"
            ).first()
            focus_confidence = 0.8
        
        if not focus_area:
            return findings
        
        # Classify issue type
        issue_type, issue_confidence = self.issue_classifier.classify(
            focus_area=focus_area,
            report_type=report_metadata.report_type,
            data={"report_type": report_metadata.report_type}
        )
        
        # Create finding for each report
        for report in reports:
            finding = Finding(
                data_source_id=data_source.id,
                soda_report_id=report.id,
                focus_area_id=focus_area.id,
                issue_type_id=issue_type.id if issue_type else None,
                title=f"{report_metadata.report_type_name} - {report.user_name or report.role_name or 'Unknown'}",
                description=f"SoDA report: {report_metadata.report_type_name}",
                severity=report.risk_level or (issue_type.default_severity if issue_type else "Medium"),
                classification_confidence=min(focus_confidence, issue_confidence) if issue_type else focus_confidence,
                detected_at=report.created_at
            )
            self.db.add(finding)
            self.db.flush()
            
            # Calculate risk assessment
            risk_data = self.risk_scorer.calculate_risk_score(finding, issue_type)
            from app.models.risk_assessment import RiskAssessment
            risk_assessment = RiskAssessment(
                finding_id=finding.id,
                **risk_data,
                risk_description=f"Risk from {report_metadata.report_type_name}",
                affected_users=1
            )
            self.db.add(risk_assessment)
            
            findings.append(finding)
        
        return findings
    
    def _group_findings(self, findings: List[Finding], analysis_run: AnalysisRun):
        """Group findings by issue type for aggregation"""
        from collections import defaultdict
        
        # Group by issue type
        grouped = defaultdict(list)
        for finding in findings:
            if finding.issue_type:
                grouped[finding.issue_type_id].append(finding)
        
        # Create issue groups
        for issue_type_id, finding_list in grouped.items():
            total_risk = sum(
                f.risk_assessment.risk_score 
                for f in finding_list 
                if f.risk_assessment
            )
            total_money_loss = sum(
                f.money_loss_calculation.estimated_loss 
                for f in finding_list 
                if f.money_loss_calculation
            )
            
            issue_group = IssueGroup(
                issue_type_id=issue_type_id,
                analysis_run_id=analysis_run.id,
                finding_count=len(finding_list),
                total_risk_score=total_risk,
                total_money_loss=total_money_loss,
                summary=f"{len(finding_list)} findings of type {finding_list[0].issue_type.name}"
            )
            self.db.add(issue_group)

