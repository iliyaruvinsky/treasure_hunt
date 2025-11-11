"""
Quick test script for uploading and analyzing files
"""
import requests
import sys
from pathlib import Path

API_BASE = "http://localhost:8000/api/v1"

def test_upload(file_path: str):
    """Test file upload"""
    print(f"\n📤 Uploading file: {file_path}")
    
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            f'{API_BASE}/ingestion/upload',
            files=files
        )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Upload successful!")
        print(f"   Data Source ID: {result['data_source_id']}")
        print(f"   Status: {result['status']}")
        print(f"   Parsed rows: {result.get('parse_result', {}).get('metadata', {}).get('data_row_count', 0)}")
        return result['data_source_id']
    else:
        print(f"❌ Upload failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return None

def test_analysis(data_source_id: int):
    """Test analysis execution"""
    print(f"\n🔍 Running analysis on data source {data_source_id}...")
    
    response = requests.post(
        f'{API_BASE}/analysis/run',
        json={'data_source_id': data_source_id}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Analysis completed!")
        print(f"   Analysis Run ID: {result['id']}")
        print(f"   Total Findings: {result['total_findings']}")
        print(f"   Findings by Focus Area: {result.get('findings_by_focus_area', {})}")
        print(f"   Total Risk Score: {result['total_risk_score']}")
        print(f"   Total Money Loss: ${result['total_money_loss']:,.2f}")
        return result['id']
    else:
        print(f"❌ Analysis failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return None

def main():
    """Main test function"""
    if len(sys.argv) < 2:
        print("Usage: python test_upload.py <file_path>")
        print("\nExample:")
        print('  python test_upload.py "../Skywind Output (Real Reports and Alerts)/4C Alerts/Summary_SAFAL SM04 Long Time Logged On Users (24+ hours) SLG_200025_000327.xlsx"')
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
    
    # Test upload
    data_source_id = test_upload(file_path)
    
    if data_source_id:
        # Test analysis
        analysis_run_id = test_analysis(data_source_id)
        
        if analysis_run_id:
            print(f"\n✅ All tests passed!")
            print(f"\nView results at:")
            print(f"   - Analysis Run: http://localhost:8000/api/v1/analysis/runs/{analysis_run_id}")
            print(f"   - API Docs: http://localhost:8000/docs")

if __name__ == "__main__":
    main()

