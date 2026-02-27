from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

from app.core.simulator import InvestmentSimulator

# from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# TODO: Remove Prometheus for now
# Instrumentator().instrument(app).expose(app)


class SimulationInput(BaseModel):
    monthly_investment: float = Field(..., ge=0)
    interest_rate: float = Field(..., ge=0)
    begin: datetime
    end: Optional[datetime]
    goal: Optional[float]
    initial_value: float = Field(..., ge=0)
    bonus: Optional[dict]


@app.post("/simulate")
def simulate(payload: SimulationInput):
    sim = InvestmentSimulator(**payload.model_dump())

    # Dict contendo valor final, data final e evolução
    result = sim.simulate()

    return result
