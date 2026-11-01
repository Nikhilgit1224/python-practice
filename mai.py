from fastapi import FastAPI

app = FastAPI(title="Practice API", version="1.0.0")


@app.get("/")
def read_root():
	return {"message": "Hello from FastAPI"}


@app.get("/health")
def read_health():
	return {"status": "ok"}
