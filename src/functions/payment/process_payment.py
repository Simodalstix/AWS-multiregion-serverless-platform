import json
import os
import boto3
import uuid
from decimal import Decimal
from typing import Dict, Any

events = None

def process_stripe_payment(amount: Decimal, currency: str = "USD", payment_method: str = "card") -> Dict[str, Any]:
    """Simulate Stripe payment processing"""
    # In real implementation, use Stripe SDK
    # import stripe
    # stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
    
    # Simulate payment processing
    payment_id = f"pi_{uuid.uuid4().hex[:24]}"
    
    # Simulate 95% success rate
    import random
    success = random.random() > 0.05
    
    if success:
        return {
            "success": True,
            "payment_id": payment_id,
            "amount": float(amount),
            "currency": currency,
            "status": "succeeded"
        }
    else:
        return {
            "success": False,
            "error": "Payment declined",
            "status": "failed"
        }

def publish_payment_event(payment_result: Dict[str, Any], order_id: str):
    """Publish payment event"""
    global events
    if events is None:
        events = boto3.client("events")
    
    event_type = "Payment Succeeded" if payment_result["success"] else "Payment Failed"
    
    events.put_events(
        Entries=[{
            "Source": "ecommerce.payments",
            "DetailType": event_type,
            "Detail": json.dumps({
                "orderId": order_id,
                "paymentId": payment_result.get("payment_id"),
                "amount": payment_result.get("amount"),
                "status": payment_result["status"]
            }),
            "EventBusName": os.environ["EVENT_BUS_ARN"].split("/")[-1]
        }]
    )

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Lambda handler for payment processing"""
    try:
        body = json.loads(event["body"])
        order_id = body["orderId"]
        amount = Decimal(str(body["amount"]))
        currency = body.get("currency", "USD")
        payment_method = body.get("paymentMethod", "card")
        
        # Process payment
        payment_result = process_stripe_payment(amount, currency, payment_method)
        
        # Publish event
        publish_payment_event(payment_result, order_id)
        
        return {
            "statusCode": 200 if payment_result["success"] else 402,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps(payment_result, default=str)
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }