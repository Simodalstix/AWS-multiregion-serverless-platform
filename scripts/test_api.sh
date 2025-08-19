#!/bin/bash

# Test E-commerce API Endpoints
set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <API_ENDPOINT>"
    echo "Example: $0 https://abc123.execute-api.ap-southeast-2.amazonaws.com/prod"
    exit 1
fi

API_URL="$1"
echo "🧪 Testing E-commerce API: $API_URL"

# Test 1: Get Products
echo "📦 Testing GET /products..."
curl -s -X GET "$API_URL/products" | jq '.'

# Test 2: Get Products by Category
echo "🔍 Testing GET /products?category=Electronics..."
curl -s -X GET "$API_URL/products?category=Electronics" | jq '.'

# Test 3: Check Inventory
echo "📊 Testing POST /inventory (check stock)..."
curl -s -X POST "$API_URL/inventory" \
  -H "Content-Type: application/json" \
  -d '{"action": "check", "productId": "prod-001", "quantity": 2}' | jq '.'

# Test 4: Create Order
echo "🛒 Testing POST /orders..."
ORDER_RESPONSE=$(curl -s -X POST "$API_URL/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "customerId": "cust-123",
    "items": [
      {"id": "prod-001", "quantity": 1, "price": 199.99},
      {"id": "prod-002", "quantity": 1, "price": 299.99}
    ]
  }')

echo "$ORDER_RESPONSE" | jq '.'
ORDER_ID=$(echo "$ORDER_RESPONSE" | jq -r '.orderId')

# Test 5: Get Order
echo "📋 Testing GET /orders/$ORDER_ID..."
curl -s -X GET "$API_URL/orders/$ORDER_ID" | jq '.'

# Test 6: Reserve Inventory
echo "🔒 Testing POST /inventory (reserve)..."
curl -s -X POST "$API_URL/inventory" \
  -H "Content-Type: application/json" \
  -d "{\"action\": \"reserve\", \"productId\": \"prod-001\", \"quantity\": 1, \"orderId\": \"$ORDER_ID\"}" | jq '.'

# Test 7: Process Payment
echo "💳 Testing POST /payments..."
curl -s -X POST "$API_URL/payments" \
  -H "Content-Type: application/json" \
  -d "{\"orderId\": \"$ORDER_ID\", \"amount\": 499.98, \"currency\": \"USD\", \"paymentMethod\": \"card\"}" | jq '.'

echo "✅ API testing completed!"