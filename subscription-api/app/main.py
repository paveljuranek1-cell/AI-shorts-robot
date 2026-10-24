from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.router import router

app = FastAPI(
    title="User Subscription Management API",
    description="A comprehensive REST API for managing user subscriptions and plans.",
    version="1.0.0",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "details": exc.errors(),
        },
    )


@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "healthy"}


app.include_router(router, prefix="/api/v1", tags=["Subscriptions"])
