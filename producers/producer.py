import json
import random
import time
import uuid
from datetime import datetime

from confluent_kafka import Producer
from faker import Faker

fake = Faker()

producer = Producer({
    "bootstrap.servers": "localhost:9092"
})

regions = ["North", "South", "East", "West", "Central"]

def create_transaction():
    return {
        "transaction_id": str(uuid.uuid4()),
        "store_id": f"STORE-{random.randint(1,100)}",
        "region": random.choice(regions),
        "customer_email": fake.email(),
        "sku": f"SKU-{random.randint(1000,9999)}",
        "quantity": random.randint(1,5),
        "unit_price": round(random.uniform(10,1000),2),
        "event_timestamp": int(datetime.now().timestamp()*1000)
    }

print("Retail Producer Started...")

while True:
    transaction = create_transaction()

    producer.produce(
        topic="pos-transactions",
        key=transaction["region"],
        value=json.dumps(transaction).encode("utf-8")
    )

    producer.poll(0)

    print(transaction)

    time.sleep(1)