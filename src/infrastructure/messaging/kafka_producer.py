import json
from confluent_kafka import Producer


class KafkaEventProducer:
    def __init__(self, bootstrap_servers: str):
        self._producer = Producer({"bootstrap.servers": bootstrap_servers})

    def publish(self, topic: str, key: str, event: dict) -> None:
        try:
            payload_str = json.dumps(event, ensure_ascii=False)
        except Exception as e:
            print("[KAFKA][ERROR] json.dumps failed:", repr(e))
            print("[KAFKA][ERROR] event type:", type(event))
            print("[KAFKA][ERROR] event value:", event)
            return

        payload = payload_str.encode("utf-8")

        def delivery_report(err, msg):
            if err is not None:
                print("[KAFKA][ERROR] delivery failed:", err)
            else:
                print(f"[KAFKA][OK] delivered to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}")

        try:
            print(f"[KAFKA] producing topic={topic} key={key} bytes={len(payload)}")
            self._producer.produce(
                topic=topic,
                key=key.encode("utf-8"),
                value=payload,
                callback=delivery_report,
            )
            self._producer.flush(10)
        except Exception as e:
            print("[KAFKA][ERROR] produce/flush failed:", repr(e))
