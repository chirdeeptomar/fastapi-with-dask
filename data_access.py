from typing import Optional

import dask.dataframe as dd
import pandas as pd
from dask.distributed import Client, Future

DASK_CLUSTER = "localhost:8786"


async def get_data(country: Optional[str] = None) -> pd.core.frame.DataFrame:
    async with Client(DASK_CLUSTER, asynchronous=True) as client:
        path = "data/*.parquet"
        if country is not None:
            predicates = [
                ("country", "==", str.capitalize(country)),
            ]
        columns = [
            "id",
            "first_name",
            "last_name",
            "country",
            "registration_dttm",
            "email",
            "gender",
            "ip_address",
            "cc",
            "birthdate",
            "salary",
            "title",
        ]

        if country:
            df: dd.DataFrame = dd.read_parquet(
                path,
                engine="pyarrow-dataset",
                columns=columns,
                filters=predicates,
            )
        else:
            df: dd.DataFrame = dd.read_parquet(
                path,
                engine="pyarrow-dataset",
                columns=columns,
            )

        future: Future = client.compute(df)
        return await future


async def get_data_for_pie() -> pd.core.frame.DataFrame:
    TOP_N = 10
    async with Client(DASK_CLUSTER, asynchronous=True) as client:
        path = "data/*.parquet"

        df: dd.DataFrame = dd.read_parquet(
            path,
            engine="pyarrow-dataset",
        )
        grouped_df = df["country"].value_counts().to_frame()
        result = (await client.compute(grouped_df)).head(TOP_N)
        countries = result.index.to_frame()
        result.merge(countries, how="cross")
        return result
