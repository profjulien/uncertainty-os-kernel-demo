"""
Uncertainty‑OS • kernel.py
Minimal heavy‑tail shock loop exposed as /tick-mini
Run:  uvicorn kernel:app --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI(title="Uncertainty‑OS Kernel v0.1‑alpha")


# ---------- request / response models ----------
class TickRequest(BaseModel):
    valuation: float          # current firm valuation ($)
    sigma: float              # volatility parameter
    action: str               # learner action id  (e.g. "burn_down")


class TickResponse(BaseModel):
    new_valuation: float
    shock: float              # % shock applied this tick
    cash_delta: float         # placeholder for later use


# ---------- endpoint ----------
@app.post("/tick-mini", response_model=TickResponse)
def tick_mini(req: TickRequest):
    """
    Applies one log‑normal multiplicative shock and a simple
    action effect; returns updated valuation.
    """
    rng = np.random.default_rng()
    shock = float(rng.lognormal(mean=0, sigma=req.sigma) - 1.0)

    # Apply learner action – placeholder deterministic effects
    cash_delta = 0.0
    if req.action == "burn_down":
        cash_delta = -0.2           # cuts burn 20 %
    elif req.action == "burn_up":
        cash_delta = 0.2            # increases burn 20 %

    new_valuation = req.valuation * (1 + shock)

    return TickResponse(
        new_valuation=new_valuation,
        shock=shock,
        cash_delta=cash_delta,
    )
