from typing import Any

from src.infrastructure.messaging.kafka_broker import KafkaMessageBroker


class FakeProducer:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def send_and_wait(
        self,
        topic: str,
        value: dict[str, Any],
        headers: list[tuple[str, bytes]] | None = None,
    ) -> None:
        self.calls.append({"topic": topic, "value": value, "headers": headers})


async def test_send_attaches_trace_id_header() -> None:
    producer = FakeProducer()
    broker = KafkaMessageBroker(producer=producer, topic="ads")  # type: ignore[arg-type]

    await broker.send(
        {"event": "ad.created", "payload": {"ad_id": 1}},
        trace_id="demo-123",
    )

    assert producer.calls == [
        {
            "topic": "ads",
            "value": {"event": "ad.created", "payload": {"ad_id": 1}},
            "headers": [("X-Trace-Id", b"demo-123")],
        }
    ]


async def test_send_without_trace_id_omits_headers() -> None:
    producer = FakeProducer()
    broker = KafkaMessageBroker(producer=producer, topic="ads")  # type: ignore[arg-type]

    await broker.send({"event": "ad.created", "payload": {"ad_id": 1}})

    assert producer.calls == [
        {
            "topic": "ads",
            "value": {"event": "ad.created", "payload": {"ad_id": 1}},
            "headers": None,
        }
    ]
