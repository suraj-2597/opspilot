from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent.investigator import investigate


app = FastAPI(
    title="OpsPilot API",
    description="AI-powered production incident investigation platform",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InvestigationRequest(BaseModel):
    incident: str


class InvestigationResponse(BaseModel):
    incident: str
    analysis: str
    timestamp: datetime


@app.get("/")
def root():
    return {
        "name": "OpsPilot",
        "status": "online",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.post(
    "/api/v1/investigate",
    response_model=InvestigationResponse,
)
def investigate_incident(
    request: InvestigationRequest,
):
    analysis = investigate(request.incident)

    return InvestigationResponse(
        incident=request.incident,
        analysis=analysis,
        timestamp=datetime.utcnow(),
    )
