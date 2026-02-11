import json
from confluent_kafka import Consumer


def main():
    consumer = Consumer({
        "bootstrap.servers": "localhost:9092",
        "group.id": "comment-changed-printer",
        "auto.offset.reset": "earliest",
    })

    consumer.subscribe(["comment.changed"])
    print("Listening: topic=comment.changed")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("Kafka error:", msg.error())
                continue

            event = json.loads(msg.value().decode("utf-8"))
            print("EVENT RECEIVED:", event)

    except KeyboardInterrupt:
        print("Stopped")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
