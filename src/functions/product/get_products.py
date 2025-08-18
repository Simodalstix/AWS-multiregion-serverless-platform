import json
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr
from typing import Dict, Any, List

dynamodb = None

def get_products(category: str = None, limit: int = 20) -> List[Dict[str, Any]]:
    """Get products from catalog"""
    global dynamodb
    if dynamodb is None:
        dynamodb = boto3.resource("dynamodb")
    
    table = dynamodb.Table(os.environ["PRODUCTS_TABLE"])
    
    if category:
        response = table.scan(
            FilterExpression=Attr('category').eq(category),
            Limit=limit
        )
    else:
        response = table.scan(Limit=limit)
    
    return response.get('Items', [])

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Lambda handler for getting products"""
    try:
        params = event.get("queryStringParameters") or {}
        category = params.get("category")
        limit = int(params.get("limit", 20))
        
        products = get_products(category, limit)
        
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"products": products}, default=str)
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }