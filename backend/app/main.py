from fastapi import FastAPI

app = FastAPI(title="OpsPilot")


@app.get("/")
def root():
    return {
        "name": "OpsPilot",
        "status": "online"
    }
