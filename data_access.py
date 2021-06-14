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


async def get_data_for_pie(group_by) -> pd.core.frame.DataFrame:
    TOP_N = 10
    async with Client(DASK_CLUSTER, asynchronous=True) as client:
        path = "data/*.parquet"

        df: dd.DataFrame = dd.read_parquet(
            path,
            engine="pyarrow-dataset",
        )
        grouped_df = df[group_by].value_counts().nlargest(TOP_N).to_frame()
        result = await client.compute(grouped_df)
        countries = result.index.to_frame()
        result.merge(countries, how="cross")
        return result


async def get_salary_data() -> pd.core.frame.DataFrame:
    async with Client(DASK_CLUSTER, asynchronous=True) as client:
        path = "data/*.parquet"

        df: dd.DataFrame = dd.read_parquet(
            path,
            engine="pyarrow-dataset",
        )
        bins = [5000, 10000, 20000, 50000, 100000, 200000, 300000, 400000, 500000]
        groups = [
            "< 10k",
            "< 20k",
            "< 50k",
            "< 100k",
            "< 200k",
            "< 300k",
            "< 400k",
            "< 500k",
        ]

        result = await client.compute(df)
        result["grouped_salary"] = pd.cut(result["salary"], bins, labels=groups)
        grouped_df = result["grouped_salary"].value_counts().to_frame()
        grouped_salary = grouped_df.index.to_frame()
        grouped_df.merge(grouped_salary, how="cross")
        return grouped_df
