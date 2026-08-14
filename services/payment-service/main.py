from fastapi import FastAPI
import time
import random

app = FastAPI(title="Payment Service")


@app.get("/health")
def health():
    return {
        "service": "payment-service",
        "status": "healthy"
    }


@app.post("/payments/{order_id}")
def process_payment(order_id: int):
    start = time.time()

    # Simulate payment processing
    time.sleep(random.uniform(0.1, 0.3))

    latency = round((time.time() - start) * 1000, 2)

    return {
        "service": "payment-service",
        "order_id": order_id,
        "status": "payment_processed",
        "latency_ms": latency
    }
