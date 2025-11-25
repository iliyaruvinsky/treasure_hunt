# AWS Deployment Guide

This directory contains AWS deployment configurations for the Treasure Hunt Analyzer.

## Prerequisites

- AWS CLI configured with appropriate credentials
- Docker installed locally
- ECR repository created for container images
- VPC and subnets configured

## Deployment Steps

### 1. Build and Push Docker Images

```bash
# Build backend image
cd ../backend
docker build -t treasure-hunt-analyzer-backend:latest .

# Build frontend image
cd ../frontend
docker build -t treasure-hunt-analyzer-frontend:latest .

# Tag and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

docker tag treasure-hunt-analyzer-backend:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/treasure-hunt-analyzer-backend:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/treasure-hunt-analyzer-backend:latest

docker tag treasure-hunt-analyzer-frontend:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/treasure-hunt-analyzer-frontend:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/treasure-hunt-analyzer-frontend:latest
```

### 2. Deploy Infrastructure with CloudFormation

```bash
aws cloudformation create-stack \
  --stack-name treasure-hunt-analyzer \
  --template-body file://cloudformation-template.yaml \
  --parameters \
    ParameterKey=Environment,ParameterValue=production \
    ParameterKey=VpcId,ParameterValue=vpc-xxxxx \
    ParameterKey=SubnetIds,ParameterValue=subnet-xxxxx,subnet-yyyyy \
  --capabilities CAPABILITY_IAM
```

### 3. Update ECS Task Definition

1. Update `ecs-task-definition.json` with your ECR image URIs
2. Register the task definition:

```bash
aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json
```

### 4. Deploy Lambda Function (Optional)

For on-demand analysis processing:

```bash
# Package Lambda function
zip lambda-function.zip lambda-function.py

# Create Lambda function
aws lambda create-function \
  --function-name tha-analysis-processor \
  --runtime python3.11 \
  --role arn:aws:iam::ACCOUNT:role/lambda-execution-role \
  --handler lambda-function.lambda_handler \
  --zip-file fileb://lambda-function.zip \
  --timeout 900 \
  --memory-size 1024
```

## Configuration

### Environment Variables

Set in ECS task definition or Lambda environment:
- `DATABASE_URL`: PostgreSQL connection string
- `STORAGE_TYPE`: `s3` for AWS deployment
- `AWS_REGION`: AWS region (e.g., `us-east-1`)
- `OPENAI_API_KEY`: From Secrets Manager
- `ANTHROPIC_API_KEY`: From Secrets Manager

### Secrets Manager

Create secrets in AWS Secrets Manager:
- `tha/database-password`: Database password
- `tha/openai-key`: OpenAI API key
- `tha/anthropic-key`: Anthropic API key

## Cost Optimization

- Use Fargate Spot for non-production environments
- Enable S3 lifecycle policies for old files
- Use RDS Multi-AZ only for production
- Consider Lambda for batch processing instead of always-on ECS

## Monitoring

- CloudWatch Logs: `/ecs/treasure-hunt-analyzer`
- CloudWatch Metrics: ECS service metrics
- RDS Performance Insights: Database monitoring

## Troubleshooting

1. Check ECS task logs in CloudWatch
2. Verify security group rules allow traffic
3. Ensure RDS is accessible from ECS tasks
4. Check S3 bucket permissions for file storage

