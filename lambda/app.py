import json
import uuid
import os
import re
from datetime import datetime

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    try:
        method = event.get("requestContext", {}).get("http", {}).get("method", "")
        path_params = event.get("pathParameters") or {}

        # =======================
        # POST /feedback
        # =======================
        if method == "POST":
            body = json.loads(event.get("body", "{}"))

            name = body.get("name")
            email = body.get("email")
            message = body.get("message")

            # Basic validation
            if not name or not email or not message:
                return {
                    "statusCode": 400,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"error": "All fields are required"})
                }

            # Email validation
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return {
                    "statusCode": 400,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"error": "Invalid email format"})
                }

            # Message length validation
            if len(message) < 5:
                return {
                    "statusCode": 400,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"error": "Message too short"})
                }

            item = {
                "id": str(uuid.uuid4()),
                "name": name,
                "email": email,
                "message": message,
                "created_at": datetime.utcnow().isoformat(),
            }

            table.put_item(Item=item)

            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "message": "Feedback submitted successfully",
                    "data": item
                })
            }

        # =======================
        # GET /feedback/{id}
        # =======================
        elif method == "GET" and path_params.get("id"):
            feedback_id = path_params.get("id")

            response = table.get_item(Key={"id": feedback_id})
            item = response.get("Item")

            if not item:
                return {
                    "statusCode": 404,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"error": "Feedback not found"})
                }

            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(item)
            }

        # =======================
        # GET /feedback (ALL)
        # =======================
        elif method == "GET":
            response = table.scan()
            items = response.get("Items", [])

            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(items)
            }

        # =======================
        # Unsupported method
        # =======================
        else:
            return {
                "statusCode": 405,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": f"Method {method} not allowed"})
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }