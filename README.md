# Serverless Multi-Region E-commerce Platform

![Architecture Overview](screenshots/AWS-multiregion-ecommerce.png)

## Overview

This project is a **serverless, event-driven e-commerce platform** built on AWS with **multi-region high availability** and **disaster recovery** capabilities. The platform demonstrates modern cloud-native architecture patterns for building scalable e-commerce applications.

### Core Features

- **Serverless Architecture**: No servers to manage, auto-scaling infrastructure
- **Multi-Region Deployment**: Active-active configuration across AWS regions (Australia + US West)
- **Event-Driven Design**: Loose coupling between services via EventBridge
- **Global Database**: DynamoDB Global Tables for multi-region data replication
- **CI/CD Pipeline**: Automated deployments via CodePipeline and CodeBuild
- **Real E-commerce Features**: Product catalog, inventory management, order processing

## Getting Started

For detailed deployment instructions, see [Getting Started Guide](docs/GETTING-STARTED.md).

Quick deployment of core infrastructure:

```bash
# Setup environment
git clone git@github.com:Simodalstix/AWS-multiregion-ecommerce.git
cd AWS-multiregion-ecommerce
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm install -g aws-cdk
aws configure

# Bootstrap CDK (one-time setup)
cdk bootstrap aws://YOUR-ACCOUNT-ID/ap-southeast-2

# Deploy core infrastructure
./deploy-core.sh

# Or manually
cdk deploy PrimaryNetworkStack PrimaryCoreStack PrimaryApiStack --app "python app-stacks.py"

# Seed sample data
python scripts/seed_data.py PrimaryCoreStack-ProductsTable PrimaryCoreStack-InventoryTable

# Test your API
API_URL=$(aws cloudformation describe-stacks --stack-name PrimaryApiStack --query 'Stacks[0].Outputs[?OutputKey==`ApiEndpoint`].OutputValue' --output text)
echo "API Endpoint: $API_URL"

curl -X POST ${API_URL}orders \
  -H "Content-Type: application/json" \
  -d '{"customerId": "123", "items": [{"id": "item1", "quantity": 1, "price": 29.99}]}'
```

## 🎯 What This Actually Does

This project gives you a **production-ready e-commerce backend** with:

- ✅ **Multi-region high availability** (Australia + US West)
- ✅ **Serverless architecture** (no servers to manage)
- ✅ **Auto-scaling** (handles any traffic volume)
- ✅ **Disaster recovery** (automatic failover capabilities)
- ✅ **Event-driven design** (extensible for new features)
- ✅ **Complete e-commerce workflow** (products, inventory, orders, payments)

## 📁 Project Structure - What Matters

```
├── app-stacks.py              # 🎯 START HERE - Deploy this first
├── infrastructure/lib/
│   ├── network_stack.py       # VPC, subnets (required)
│   ├── core_services_stack.py # DynamoDB tables (required)
│   ├── api_compute_stack.py   # API Gateway + Lambda (required)
│   └── pipeline_stack.py      # CI/CD (optional - for automation)
├── src/functions/             # Your actual business logic
│   ├── order/                 # Order management
│   ├── inventory/             # Inventory tracking
│   ├── payment/               # Payment processing
│   └── notification/          # Customer notifications
└── docs/                      # Documentation
```

## 🎯 Deployment Options - Pick Your Path

### Option 1: Manual Deployment (Recommended for Learning)

Deploy stacks directly using CDK:

```bash
# Deploy core infrastructure only (ignore security for now)
cdk deploy PrimaryNetworkStack PrimaryCoreStack PrimaryApiStack --app "python app-stacks.py"

# Later, add secondary region for disaster recovery
cdk deploy SecondaryNetworkStack SecondaryCoreStack SecondaryApiStack --app "python app-stacks.py"
```

### Option 2: CI/CD Pipeline (For Production)

Automatically deploy on git push:

```bash
# 1. Store GitHub token in AWS Secrets Manager
aws secretsmanager create-secret --name github-token --secret-string "your-github-token"

# 2. Deploy pipeline
cdk deploy PipelineStack

# 3. Now any git push to main automatically deploys!
```

## 🔧 Testing Your Deployment

### Unit Tests

```bash
python -m pytest tests/ -v
```

### API Testing

```bash
# Get your API endpoint
aws cloudformation describe-stacks --stack-name PrimaryApiStack --query 'Stacks[0].Outputs'

# Use the test script
./scripts/test_api.sh https://YOUR-API-URL/prod

# Or test manually
curl -X GET https://YOUR-API-URL/prod/products
curl -X POST https://YOUR-API-URL/prod/orders \
  -H "Content-Type: application/json" \
  -d '{"customerId": "123", "items": [{"id": "prod-001", "quantity": 1, "price": 199.99}]}'
```

## 🛒 E-commerce Features

The platform includes complete e-commerce functionality:

- **Product Catalog**: Browse and search products with categories
- **Inventory Management**: Real-time stock tracking with atomic updates
- **Order Processing**: Complete order lifecycle with event-driven workflow
- **Payment Integration**: Simulated payment processing (Stripe-ready)
- **Event-Driven Architecture**: EventBridge for loose coupling
- **Multi-region Sync**: DynamoDB Global Tables for data consistency

### API Endpoints

```bash
# Products
GET /products                    # List all products
GET /products?category=Electronics  # Filter by category

# Orders
POST /orders                     # Create new order
GET /orders/{orderId}            # Get order details

# Inventory
POST /inventory                  # Check/reserve stock

# Payments
POST /payments                   # Process payment
```

## 📚 Detailed Documentation

- [Setup Guide](docs/setup.md) - Complete setup instructions
- [Architecture](docs/architecture.md) - Technical architecture details
- [Getting Started](docs/GETTING-STARTED.md) - Quick start guide

## 🎯 Inspiration & Learning Resources

This project demonstrates patterns from these excellent resources:

### AWS Architecture Blogs
- [Building event-driven architectures on AWS](https://aws.amazon.com/blogs/compute/building-event-driven-architectures-on-aws/)
- [Multi-Region Serverless Backend](https://aws.amazon.com/blogs/compute/building-a-multi-region-serverless-backend-for-a-web-application/)
- [DynamoDB Global Tables Best Practices](https://aws.amazon.com/blogs/database/how-to-use-amazon-dynamodb-global-tables-to-power-multiregion-architecture/)

### Serverless E-commerce Patterns
- [Serverless E-commerce Platform on AWS](https://aws.amazon.com/solutions/implementations/serverless-ecommerce-platform/)
- [Event-driven microservices with EventBridge](https://aws.amazon.com/blogs/compute/using-amazon-eventbridge-to-build-decoupled-fault-tolerant-applications/)
- [Building resilient serverless systems](https://aws.amazon.com/builders-library/reliability-and-constant-work/)

### Real-World Implementation Examples
- **Netflix**: Multi-region disaster recovery patterns
- **Airbnb**: Event-driven inventory management
- **Stripe**: Payment processing architecture patterns

## 🎯 Key Files You Should Know

| File                                                          | Purpose                     | When to Use                          |
| ------------------------------------------------------------- | --------------------------- | ------------------------------------ |
| [`app-stacks.py`](app-stacks.py:1)                            | Main deployment entry point | **Start here for manual deployment** |
| [`pipeline_stack.py`](infrastructure/lib/pipeline_stack.py:1) | CI/CD pipeline              | For automated deployments            |
| [`requirements.txt`](requirements.txt:1)                      | Python dependencies         | Install before deploying             |
| [`cdk.json`](cdk.json:1)                                      | CDK configuration           | Modify for custom settings           |

## 🚨 Common Issues and Solutions

1. **"cdk: command not found"**

   ```bash
   npm install -g aws-cdk
   ```

2. **Bootstrap errors**

   ```bash
   cdk bootstrap aws://YOUR-ACCOUNT-ID/YOUR-REGION
   ```

3. **Permission denied**
   Make sure your AWS user has AdministratorAccess policy

## 📞 Support

For issues and feature requests, please create an issue in the GitHub repository.
