import time
import uuid
from typing import List
from fastapi import FastAPI, Request, Response, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# Exact allowed origin assigned to you
ALLOWED_ORIGIN = "https://dash-5c4z1z.example.com"

# Standard FastAPI CORS Middleware for the single origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

# Required middleware for X-Request-ID and X-Process-Time headers on every response
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    return response

@app.get("/stats")
async def get_stats(values: str = Query(..., description="Comma-separated integers")):
    try:
        # Parse comma-separated integers
        nums: List[int] = [int(v.strip()) for v in values.split(",") if v.strip()]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid integers provided in query parameter.")
    
    if not nums:
        raise HTTPException(status_code=400, detail="No integers found.")
    
    count = len(nums)
    total_sum = sum(nums)
    min_val = min(nums)
    max_val = max(nums)
    mean_val = round(total_sum / count, 4)
    
    return {
        "email": "24f2006714@ds.study.iitm.ac.in",
        "count": count,
        "sum": total_sum,
        "min": min_val,
        "max": max_val,
        "mean": mean_val
    }