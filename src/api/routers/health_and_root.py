from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "healthy"}

@router.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the FastAPI application!"}