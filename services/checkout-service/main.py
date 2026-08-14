from fastapi import FastAPI
import time
import requests

app = FastAPI(title="Checkout Service")

ORDER_SERVICE = "http://127.0.0.1:8002"
PAYMENT_SERVICE = "http://127.0.0.1:8003"


@app.get("/health")
def health():
    return {
        "service": "checkout-service",
        "status": "healthy"
    }


@app.post("/checkout/{order_id}")
def checkout(order_id: int):
    start = time.time()

    order_response = requests.get(
        f"{ORDER_SERVICE}/orders/{order_id}"
    )

    if order_response.status_code != 200:
        return {
            "service": "checkout-service",
            "status": "order_failed"
        }

    payment_response = requests.post(
        f"{PAYMENT_SERVICE}/payments/{order_id}"
    )

    if payment_response.status_code != 200:
        return {
            "service": "checkout-service",
            "status": "payment_failed"
        }

    latency = round((time.time() - start) * 1000, 2)

    return {
        "service": "checkout-service",
        "order_id": order_id,
        "status": "checkout_success",
        "latency_ms": latency
    }
