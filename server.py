import json
import time
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from data_access import get_data, get_data_for_pie

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/data/{country}")
async def read_data(country: Optional[str] = None):
    begin = time.time()
    result = await get_data(country)
    parsed = json.loads(result.to_json(orient="records"))
    return {
        "time(secs)": (time.time() - begin),
        "result": parsed,
    }


@app.get("/pie")
async def make_pie():
    begin = time.time()
    result = await get_data_for_pie()
    parsed = json.loads(result.to_json())
    return {
        "time(secs)": (time.time() - begin),
        "result": parsed,
    }
