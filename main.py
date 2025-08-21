from fastapi import FastAPI, Body


app = FastAPI()

@app.post("/posts/")
def add_post(payload: dict ):
    return payload


