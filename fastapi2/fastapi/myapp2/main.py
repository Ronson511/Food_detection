import requests
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "API"}


@app.get("/domain/{domain}")
def get_domain(domain: str):
    response = requests.get("http://ip-api.com/json/" + domain)
    return response.json()