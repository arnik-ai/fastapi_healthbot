from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import connect_to_mongo, close_mongo_connection
from routers import patient, doctor, health_metrics, medical_file, record


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    try:
        yield
    finally:
        await close_mongo_connection()


app = FastAPI(title="HealthAPI", version="1.0.0", lifespan=lifespan)


# CORS (برای اتصال Streamlit یا فرانت)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(patient.router, prefix="/patients", tags=["patients"])
app.include_router(doctor.router, prefix="/doctors", tags=["doctors"])
app.include_router(health_metrics.router, prefix="/health-metrics", tags=["health-metrics"])
app.include_router(medical_file.router, prefix="/files", tags=["files"])
app.include_router(record.router, prefix="/records", tags=["records"])


@app.get("/")
async def root():
    return {"message": "HealthAPI is running!"}
