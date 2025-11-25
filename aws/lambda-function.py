"""
AWS Lambda function for on-demand analysis processing
Can be triggered by S3 uploads, EventBridge, or API Gateway
"""
import json
import os
import boto3
from typing import Dict, Any

# Initialize clients
s3_client = boto3.client('s3')
rds_client = boto3.client('rds')
secrets_manager = boto3.client('secretsmanager')

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for processing analysis requests
    
    Event structure:
    {
        "data_source_id": 123,
        "action": "analyze"
    }
    """
    try:
        # Extract parameters
        data_source_id = event.get('data_source_id')
        action = event.get('action', 'analyze')
        
        if not data_source_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'data_source_id is required'})
            }
        
        # Get database connection from RDS
        db_url = get_database_url()
        
        # Import analysis engine (would need to be packaged with Lambda)
        # from app.services.analysis.analyzer import Analyzer
        # analyzer = Analyzer(db_session)
        # result = analyzer.analyze_data_source(data_source_id)
        
        # For now, return mock response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Analysis {action} initiated for data_source_id: {data_source_id}',
                'data_source_id': data_source_id
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def get_database_url() -> str:
    """Get database URL from Secrets Manager"""
    secret_name = os.environ.get('DB_SECRET_NAME', 'tha/database')
    response = secrets_manager.get_secret_value(SecretId=secret_name)
    secret = json.loads(response['SecretString'])
    return secret['connection_string']

