import boto3
import uuid


def add_recommendation(name, user_id):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("is-it-vegan-recommendations")
    table.put_item(
        Item={
            "id": uuid.uuid4().hex,
            "name": name,
            "user_id": user_id
        }
    )
