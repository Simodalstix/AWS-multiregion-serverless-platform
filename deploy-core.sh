#!/bin/bash

# Deploy Core E-commerce Infrastructure
# This script deploys only the essential stacks for the e-commerce platform

set -e

echo "🚀 Deploying Core E-commerce Infrastructure..."

# Deploy Primary Region (Australia)
echo "📍 Deploying Primary Region (Australia)..."
cdk deploy PrimaryNetworkStack PrimaryCoreStack PrimaryApiStack \
  --app "python app-stacks.py" \
  --require-approval never

# Deploy Secondary Region (US West)
echo "📍 Deploying Secondary Region (US West)..."
cdk deploy SecondaryNetworkStack SecondaryCoreStack SecondaryApiStack \
  --app "python app-stacks.py" \
  --require-approval never

echo "✅ Core infrastructure deployed successfully!"

# Get API endpoints
echo "🔗 API Endpoints:"
echo "Primary (Australia): $(aws cloudformation describe-stacks --stack-name PrimaryApiStack --query 'Stacks[0].Outputs[?OutputKey==`ApiEndpoint`].OutputValue' --output text --region ap-southeast-2)"
echo "Secondary (US West): $(aws cloudformation describe-stacks --stack-name SecondaryApiStack --query 'Stacks[0].Outputs[?OutputKey==`ApiEndpoint`].OutputValue' --output text --region us-west-2)"

echo "🎉 Ready to build your e-commerce platform!"