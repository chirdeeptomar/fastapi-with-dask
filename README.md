# REST API + DASK

Sample code demonstrating usage of DASK from FastAPI. Application queries parquet dataset using Dask APIs.

Steps to run: 

1) Set up a virtual environment for Python 3 and enable it
2) Run command `pip install -r requirements.txt` to install the dependencies
3) Run command `dask-scheduler` to start Dask Schedular, you can visit the dashboard here: http://localhost:8787/status
4) Run command `dask-worker localhost:8786` to start Dask worker
5) Run command `uvicorn server:app --reload --port 8090` to start the ASGI web server
6) Launch Swagger at http://localhost:8090/docs/ 
7) Invoke HTTP via curl using command `curl -XGET http://localhost:8090/data/India`
8) You should see the results as below:

```json
{
    "result": [
        {
            "id": 596,
            "first_name": "Robin",
            "last_name": "Carter",
            "country": "India"
        },
        {
            "id": 182,
            "first_name": "Donna",
            "last_name": "Boyd",
            "country": "India"
        }
    ]
}
```
