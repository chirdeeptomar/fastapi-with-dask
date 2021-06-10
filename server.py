import json
import time

import dask.dataframe as dd
from dask.distributed import Client
from fastapi import FastAPI
from pandas.core.frame import DataFrame

DASK_CLUSTER = "localhost:8786"

app = FastAPI()


async def get_data(country) -> DataFrame:
    async with Client(DASK_CLUSTER, asynchronous=True) as client:
        path = "data/*.parquet"
        predicates = [
            ("country", "==", str.capitalize(country)),
        ]
        columns = [
            "id",
            "first_name",
            "last_name",
            "country",
        ]

        df = dd.read_parquet(
            path, engine="pyarrow-dataset", columns=columns, filters=predicates
        )
        future = client.compute(df)
        return await future


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/data/{country}")
async def read_data(country: str):
    begin = time.time()
    result = await get_data(country)
    parsed = json.loads(result.to_json(orient="records"))
    return {
        "time(secs)": (time.time() - begin),
        "result": parsed,
    }
