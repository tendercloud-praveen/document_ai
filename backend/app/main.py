from fastapi import FastAPI
from app.api.documents import router
from app.database.database import engine
from app.database.database import Base
from app.api.approval import router as approval_router
from app.api.update import router as update_router

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(router)
app.include_router(approval_router)
app.include_router(update_router)

@app.get("/")
async def root():
    return {"message": "Document AI Backend is running!"}