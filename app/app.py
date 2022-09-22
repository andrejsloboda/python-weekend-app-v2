import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.api.v1.router import v1_api_router


app = FastAPI()


@app.on_event("startup")
def startup_event():
    pass


@app.on_event("shutdown")
def shutdown_event():
    pass


# API configuration for front-end
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["application/json"]
)

app.include_router(v1_api_router)

if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
