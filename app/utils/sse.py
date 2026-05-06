import json
import os
import redis


redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", "6379"))

# decode_responses=True to get strings instead of bytes
redis_client = redis.Redis(
    host=redis_host, port=redis_port, db=0, decode_responses=True)


def notify_clients(board_id, data):
    channel = f"board_{board_id}"
    redis_client.publish(channel, json.dumps(data))


def get_board_stream(board_id):
    pubsub = redis_client.pubsub()
    channel = f"board_{board_id}"
    pubsub.subscribe(channel)

    for message in pubsub.listen():  # loop blocks until redis publishes smt
        if message["type"] == "message":
            yield f"data: {message['data']}\n\n" # yield turns function into generator so instead of returning, it can send a value, pause, then continue
