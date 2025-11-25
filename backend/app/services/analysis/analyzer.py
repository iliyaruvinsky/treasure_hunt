from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import traceback
import logging

from app.models.data_source import DataSource
from app.models.alert import Alert, AlertMetadata
from app.models.soda_report import SoDAReport, SoDAReportMetadata
from app.models.finding import Finding
from app.models.analysis_run import AnalysisRun
from app.models.issue_type import IssueGroup
from app.models.focus_area import FocusArea

from .classifier import FocusAreaClassifier, IssueTypeClassifier
from .risk_scorer import RiskScorer
from app.services.hybrid_engine import HybridMoneyLossEngine

logger = logging.getLogger(__name__)


class Analyzer:
    """Main analysis engine that processes data sources and creates findings"""
    
    def __init__(self, db: Session):
        self.db = db
        self.focus_classifier = FocusAreaClassifier(db)
        self.issue_classifier = IssueTypeClassifier(db)
        self.risk_scorer = RiskScorer()
        self.money_loss_calculator = HybridMoneyLossEngine()
    
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
            started_at=datetime.utcnow(),
            data_source_id=data_source.id
        )
        self.db.add(analysis_run)
        self.db.commit()
        
        try:
            findings = []
            
            # Process based on data type
            # Handle both enum and string values
            data_type_value = data_source.data_type.value if hasattr(data_source.data_type, 'value') else str(data_source.data_type)
            if data_type_value == "alert":
                findings = self._analyze_alert(data_source, analysis_run)
            elif data_type_value == "report":
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
            error_traceback = traceback.format_exc()
            logger.error(f"Analysis failed for data_source_id={data_source_id}: {str(e)}\n{error_traceback}")
            print(f"ERROR in analyze_data_source: {str(e)}")
            print(error_traceback)
            analysis_run.status = "failed"
            analysis_run.error_message = f"{str(e)}\n{error_traceback[:500]}"  # Limit error message length
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
            logger.warning(f"No alert metadata found for data_source_id={data_source.id}")
            return findings
        
        # Get alerts
        alerts = self.db.query(Alert).filter(
            Alert.data_source_id == data_source.id
        ).all()
        
        if not alerts:
            logger.warning(f"No alerts found for data_source_id={data_source.id}")
            return findings
        
        # Classify focus area
        focus_area, focus_confidence = self.focus_classifier.classify(
            alert_name=alert_metadata.alert_name,
            data={"alert_id": alert_metadata.alert_id}
        )
        
        if not focus_area:
            # Try to get a default focus area based on filename patterns
            filename_lower = data_source.filename.lower()
            if 'print' in filename_lower or 'spool' in filename_lower or 'sp01' in filename_lower:
                focus_area = self.db.query(FocusArea).filter(FocusArea.code == "TECHNICAL_CONTROL").first()
                focus_confidence = 0.7
            elif 'sales' in filename_lower or 'order' in filename_lower or 'customer' in filename_lower:
                focus_area = self.db.query(FocusArea).filter(FocusArea.code == "BUSINESS_CONTROL").first()
                focus_confidence = 0.7
            elif 'vendor' in filename_lower or 'payment' in filename_lower:
                focus_area = self.db.query(FocusArea).filter(FocusArea.code == "BUSINESS_PROTECTION").first()
                focus_confidence = 0.7
            elif 'logged' in filename_lower or 'session' in filename_lower or 'user' in filename_lower:
                focus_area = self.db.query(FocusArea).filter(FocusArea.code == "ACCESS_GOVERNANCE").first()
                focus_confidence = 0.7
        
        if not focus_area:
            logger.warning(f"Could not classify focus area for alert: {alert_metadata.alert_name}")
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
            # Filter out fields that aren't in RiskAssessment model
            allowed_fields = {'risk_score', 'risk_level', 'risk_category', 'risk_factors', 'potential_impact', 'affected_systems'}
            filtered_risk_data = {k: v for k, v in risk_data.items() if k in allowed_fields}
            risk_assessment = RiskAssessment(
                finding_id=finding.id,
                **filtered_risk_data,
                risk_description=f"Risk associated with {alert_metadata.alert_name}",
                affected_users=1
            )
            self.db.add(risk_assessment)
            self.db.flush()  # Flush to ensure risk_assessment is available for money loss calculation
            
            # Calculate money loss
            try:
                money_loss_data = self.money_loss_calculator.calculate(
                    finding=finding,
                    issue_type=issue_type,
                    additional_context={
                        "alert_name": alert_metadata.alert_name,
                        "alert_id": alert_metadata.alert_id,
                        "user_name": alert.user_name,
                    },
                    use_llm=False,  # Disable LLM for now to avoid API calls, use ML only
                    use_ml=True
                )
                
                from app.models.money_loss import MoneyLossCalculation
                money_loss_calc = MoneyLossCalculation(
                    finding_id=finding.id,
                    estimated_loss=float(money_loss_data.get("estimated_loss", 0.0)),
                    confidence_score=float(money_loss_data.get("confidence", 0.5)),
                    calculation_method=money_loss_data.get("calculation_method", "ml"),
                    reasoning=money_loss_data.get("reasoning", "")[:1000] if money_loss_data.get("reasoning") else None,
                    factors_considered=money_loss_data.get("factors_considered", []),
                    llm_estimate=money_loss_data.get("llm_estimate"),
                    ml_estimate=money_loss_data.get("ml_estimate"),
                    final_estimate=float(money_loss_data.get("estimated_loss", 0.0))
                )
                self.db.add(money_loss_calc)
            except Exception as e:
                logger.warning(f"Failed to calculate money loss for finding {finding.id}: {str(e)}")
                # Create a default money loss calculation
                from app.models.money_loss import MoneyLossCalculation
                money_loss_calc = MoneyLossCalculation(
                    finding_id=finding.id,
                    estimated_loss=0.0,
                    confidence_score=0.0,
                    calculation_method="failed",
                    reasoning=f"Calculation failed: {str(e)}"
                )
                self.db.add(money_loss_calc)
            
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
        # Use report_type as report_type_name is not in the model
        report_type_name = report_metadata.report_type or "Unknown Report"
        
        for report in reports:
            finding = Finding(
                data_source_id=data_source.id,
                soda_report_id=report.id,
                focus_area_id=focus_area.id,
                issue_type_id=issue_type.id if issue_type else None,
                title=f"{report_type_name} - {report.user_name or report.role_name or 'Unknown'}",
                description=f"SoDA report: {report_type_name}",
                severity=report.risk_level or (issue_type.default_severity if issue_type else "Medium"),
                classification_confidence=min(focus_confidence, issue_confidence) if issue_type else focus_confidence,
                detected_at=report.created_at
            )
            self.db.add(finding)
            self.db.flush()
            
            # Calculate risk assessment
            risk_data = self.risk_scorer.calculate_risk_score(finding, issue_type)
            from app.models.risk_assessment import RiskAssessment
            # Filter out fields that aren't in RiskAssessment model
            allowed_fields = {'risk_score', 'risk_level', 'risk_category', 'risk_factors', 'potential_impact', 'affected_systems'}
            filtered_risk_data = {k: v for k, v in risk_data.items() if k in allowed_fields}
            risk_assessment = RiskAssessment(
                finding_id=finding.id,
                **filtered_risk_data,
                risk_description=f"Risk from {report_type_name}",
                affected_users=1
            )
            self.db.add(risk_assessment)
            self.db.flush()  # Flush to ensure risk_assessment is available for money loss calculation
            
            # Calculate money loss
            try:
                money_loss_data = self.money_loss_calculator.calculate(
                    finding=finding,
                    issue_type=issue_type,
                    additional_context={
                        "report_type": report_metadata.report_type,
                        "user_name": report.user_name,
                        "role_name": report.role_name,
                    },
                    use_llm=False,  # Disable LLM for now to avoid API calls, use ML only
                    use_ml=True
                )
                
                from app.models.money_loss import MoneyLossCalculation
                money_loss_calc = MoneyLossCalculation(
                    finding_id=finding.id,
                    estimated_loss=float(money_loss_data.get("estimated_loss", 0.0)),
                    confidence_score=float(money_loss_data.get("confidence", 0.5)),
                    calculation_method=money_loss_data.get("calculation_method", "ml"),
                    reasoning=money_loss_data.get("reasoning", "")[:1000] if money_loss_data.get("reasoning") else None,
                    factors_considered=money_loss_data.get("factors_considered", []),
                    llm_estimate=money_loss_data.get("llm_estimate"),
                    ml_estimate=money_loss_data.get("ml_estimate"),
                    final_estimate=float(money_loss_data.get("estimated_loss", 0.0))
                )
                self.db.add(money_loss_calc)
            except Exception as e:
                logger.warning(f"Failed to calculate money loss for finding {finding.id}: {str(e)}")
                # Create a default money loss calculation
                from app.models.money_loss import MoneyLossCalculation
                money_loss_calc = MoneyLossCalculation(
                    finding_id=finding.id,
                    estimated_loss=0.0,
                    confidence_score=0.0,
                    calculation_method="failed",
                    reasoning=f"Calculation failed: {str(e)}"
                )
                self.db.add(money_loss_calc)
            
            findings.append(finding)
        
        return findings
    
    def _group_findings(self, findings: List[Finding], analysis_run: AnalysisRun):
        """Group findings by issue type for aggregation"""
        from collections import defaultdict
        
        if not findings:
            return  # No findings to group
        
        # Group by issue type
        grouped = defaultdict(list)
        for finding in findings:
            if finding.issue_type and finding.issue_type_id:
                grouped[finding.issue_type_id].append(finding)
        
        if not grouped:
            return  # No findings with issue types to group
        
        # Create issue groups
        for issue_type_id, finding_list in grouped.items():
            if not finding_list:
                continue
                
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
            
            issue_type_name = finding_list[0].issue_type.name if finding_list[0].issue_type else "Unknown"
            issue_group = IssueGroup(
                issue_type_id=issue_type_id,
                analysis_run_id=analysis_run.id,
                finding_count=len(finding_list),
                total_risk_score=total_risk,
                total_money_loss=total_money_loss,
                summary=f"{len(finding_list)} findings of type {issue_type_name}"
            )
            self.db.add(issue_group)

