from fastapi import FastAPI

app = FastAPI(title="Numervia API")


@app.get("/api/v1/health")
def health():
    return {"status": "ok"}