#!/usr/bin/env python3
"""
Seed sample data for the e-commerce platform
"""
import boto3
import json
from decimal import Decimal

def seed_products(table_name: str, region: str = "ap-southeast-2"):
    """Seed products table with sample data"""
    dynamodb = boto3.resource("dynamodb", region_name=region)
    table = dynamodb.Table(table_name)
    
    products = [
        {
            "productId": "prod-001",
            "name": "Wireless Headphones",
            "description": "Premium noise-cancelling wireless headphones",
            "price": Decimal("199.99"),
            "category": "Electronics",
            "brand": "TechCorp",
            "imageUrl": "https://example.com/headphones.jpg"
        },
        {
            "productId": "prod-002", 
            "name": "Smart Watch",
            "description": "Fitness tracking smartwatch with GPS",
            "price": Decimal("299.99"),
            "category": "Electronics",
            "brand": "FitTech",
            "imageUrl": "https://example.com/smartwatch.jpg"
        },
        {
            "productId": "prod-003",
            "name": "Coffee Maker",
            "description": "Programmable drip coffee maker",
            "price": Decimal("89.99"),
            "category": "Home",
            "brand": "BrewMaster",
            "imageUrl": "https://example.com/coffee.jpg"
        },
        {
            "productId": "prod-004",
            "name": "Running Shoes",
            "description": "Lightweight running shoes for all terrains",
            "price": Decimal("129.99"),
            "category": "Sports",
            "brand": "RunFast",
            "imageUrl": "https://example.com/shoes.jpg"
        }
    ]
    
    with table.batch_writer() as batch:
        for product in products:
            batch.put_item(Item=product)
    
    print(f"✅ Seeded {len(products)} products")

def seed_inventory(table_name: str, region: str = "ap-southeast-2"):
    """Seed inventory table with sample data"""
    dynamodb = boto3.resource("dynamodb", region_name=region)
    table = dynamodb.Table(table_name)
    
    inventory = [
        {"productId": "prod-001", "stock": 50, "reserved": 0},
        {"productId": "prod-002", "stock": 25, "reserved": 0},
        {"productId": "prod-003", "stock": 100, "reserved": 0},
        {"productId": "prod-004", "stock": 75, "reserved": 0}
    ]
    
    with table.batch_writer() as batch:
        for item in inventory:
            batch.put_item(Item=item)
    
    print(f"✅ Seeded {len(inventory)} inventory items")

def main():
    """Main seeding function"""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python seed_data.py <products_table> <inventory_table> [region]")
        sys.exit(1)
    
    products_table = sys.argv[1]
    inventory_table = sys.argv[2]
    region = sys.argv[3] if len(sys.argv) > 3 else "ap-southeast-2"
    
    print(f"🌱 Seeding data in region: {region}")
    
    try:
        seed_products(products_table, region)
        seed_inventory(inventory_table, region)
        print("🎉 Data seeding completed successfully!")
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()