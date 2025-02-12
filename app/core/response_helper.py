import json
from fastapi import Response


def send_response(message: str = None, data: str = None, status_code: int = 200):
    payload = {}

    if message:
        payload["message"] = message

    if data:
        payload["data"] = data

    # Send an empty array if data is an empty list
    if isinstance(data, list) and len(data) == 0:
        payload["data"] = []


    return Response(
        content=json.dumps(payload),
        status_code=status_code,
        media_type="application/json",
    )
