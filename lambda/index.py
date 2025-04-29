# lambda/index.py
import json
import urllib.request
import re

API_URL = "https://5c93-34-16-161-159.ngrok-free.app"  # ← あなたのColabのURLに置き換えて

import json
import urllib.request

def lambda_handler(event, context):
    message = event["message"]  # Lambdaイベントの中のmessageを取り出す
    url = "https://xxxxxx.ngrok.io/predict"  # Colabで立てたFastAPIサーバーのURL（ngrokのURLに置き換えてください）
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({"message": message}).encode("utf-8")  # messageをJSON形式にエンコード

    # FastAPIにPOSTリクエストを送信
    req = urllib.request.Request(url, data=data, headers=headers)

    # サーバーからの応答を受け取る
    with urllib.request.urlopen(req) as res:
        result = json.load(res)  # JSONレスポンスを読み込む

    # 応答を返す
    return {
        "statusCode": 200,
        "body": result["response"]  # FastAPIから返されたresponseを取得
    }


