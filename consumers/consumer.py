from kafka import KafkaConsumer
import json
import os
from datetime import datetime

KAFKA_SERVER = "localhost:9092"
TOPIC = "pos-transactions"

BRONZE_DIR = "landing/bronze"

os.makedirs(BRONZE_DIR, exist_ok=True)

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("=" * 60)
print("KAFKA CONSUMER STARTED")
print("=" * 60)

for message in consumer:

    data = message.value

    print(data)

    filename = datetime.now().strftime("%Y%m%d") + ".json"

    filepath = os.path.join(BRONZE_DIR, filename)

    with open(filepath, "a") as f:
        json.dump(data, f)
        f.write("\n")
