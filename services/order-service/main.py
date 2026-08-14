from fastapi import FastAPI
import time
import random

app = FastAPI(title="Order Service")


@app.get("/health")
def health():
    return {
        "service": "order-service",
        "status": "healthy"
    }


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    start = time.time()

    # Simulate database lookup
    time.sleep(random.uniform(0.05, 0.15))

    latency = round((time.time() - start) * 1000, 2)

    return {
        "service": "order-service",
        "order_id": order_id,
        "status": "found",
        "latency_ms": latency
    }
