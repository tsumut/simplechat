# lambda/index.py
import json
import urllib.request
import re

API_URL = "https://d719-34-150-138-12.ngrok-free.app/"  # ← あなたのColabのURLに置き換えて！

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))

        user_info = None
        if 'requestContext' in event and 'authorizer' in event['requestContext']:
            user_info = event['requestContext']['authorizer']['claims']
            print(f"Authenticated user: {user_info.get('email') or user_info.get('cognito:username')}")

        body = json.loads(event['body'])
        message = body['message']
        print("Sending message to external API:", message)

        data = json.dumps({"message": message}).encode("utf-8")
        req = urllib.request.Request(
            API_URL,
            data=data,
            headers={"Content-Type": "application/json"}
        )

        with urllib.request.urlopen(req) as res:
            api_response = json.loads(res.read().decode())

        assistant_response = api_response.get("response", "No response received")

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": True,
                "response": assistant_response,
                "conversationHistory": [
                    {"role": "user", "content": message},
                    {"role": "assistant", "content": assistant_response}
                ]
            })
        }

    except Exception as error:
        print("Error:", str(error))

        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": False,
                "error": str(error)
            })
        }
cd ..
git add lambda/index.py
git commit -m "FastAPIを呼び出すようにlambdaを修正"
git push origin main


