import json
import os
import boto3
from typing import Dict, Any

dynamodb = None
events = None

def check_inventory(product_id: str, quantity: int) -> Dict[str, Any]:
    """Check if product is in stock"""
    global dynamodb
    if dynamodb is None:
        dynamodb = boto3.resource("dynamodb")
    
    table = dynamodb.Table(os.environ["INVENTORY_TABLE"])
    
    try:
        response = table.get_item(Key={"productId": product_id})
        item = response.get("Item")
        
        if not item:
            return {"available": False, "reason": "Product not found"}
        
        available_stock = item.get("stock", 0)
        
        if available_stock >= quantity:
            return {"available": True, "stock": available_stock}
        else:
            return {"available": False, "reason": f"Insufficient stock. Available: {available_stock}"}
    
    except Exception as e:
        return {"available": False, "reason": f"Error checking stock: {str(e)}"}

def reserve_inventory(product_id: str, quantity: int, order_id: str) -> bool:
    """Reserve inventory for an order"""
    global dynamodb
    if dynamodb is None:
        dynamodb = boto3.resource("dynamodb")
    
    table = dynamodb.Table(os.environ["INVENTORY_TABLE"])
    
    try:
        # Atomic update to reduce stock
        response = table.update_item(
            Key={"productId": product_id},
            UpdateExpression="SET stock = stock - :qty, reserved = reserved + :qty",
            ConditionExpression="stock >= :qty",
            ExpressionAttributeValues={":qty": quantity},
            ReturnValues="UPDATED_NEW"
        )
        
        # Publish inventory event
        publish_inventory_event(product_id, "RESERVED", quantity, order_id)
        return True
        
    except Exception:
        return False

def publish_inventory_event(product_id: str, action: str, quantity: int, order_id: str):
    """Publish inventory change event"""
    global events
    if events is None:
        events = boto3.client("events")
    
    events.put_events(
        Entries=[{
            "Source": "ecommerce.inventory",
            "DetailType": f"Inventory {action}",
            "Detail": json.dumps({
                "productId": product_id,
                "quantity": quantity,
                "orderId": order_id,
                "action": action
            }),
            "EventBusName": os.environ["EVENT_BUS_ARN"].split("/")[-1]
        }]
    )

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Lambda handler for inventory operations"""
    try:
        body = json.loads(event["body"])
        action = body.get("action", "check")
        product_id = body["productId"]
        quantity = body["quantity"]
        
        if action == "check":
            result = check_inventory(product_id, quantity)
            return {
                "statusCode": 200,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps(result)
            }
        
        elif action == "reserve":
            order_id = body["orderId"]
            success = reserve_inventory(product_id, quantity, order_id)
            return {
                "statusCode": 200 if success else 409,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"success": success})
            }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }