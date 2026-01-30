from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy.exc import SQLAlchemyError
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine
from app.models.user import Base
from app.api.v1.router import api_router
from app.middleware.cors import setup_cors
from app.middleware.error_handler import (
    validation_exception_handler,
    sqlalchemy_exception_handler,
    general_exception_handler
)
from app.middleware.rate_limiter import RateLimiter
from app.utils.logger import setup_logger

# Setup logger
logger = setup_logger(__name__, "logs/app.log")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("Starting application...")
    # Create tables (for development only, use Alembic in production)
    Base.metadata.create_all(bind=engine)
    logger.info("Application started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    logger.info("Application shut down successfully")

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/swagger",
    redoc_url=None,  # Disable default ReDoc to use custom
    lifespan=lifespan
)

# Setup CORS
setup_cors(app)

# Add rate limiting middleware
app.middleware("http")(RateLimiter(requests_per_minute=100))

# Exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)  # type: ignore
app.add_exception_handler(Exception, general_exception_handler)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "service": settings.PROJECT_NAME
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "docs": f"{settings.API_V1_STR}/docs"
    }

# Custom ReDoc endpoint with stable CDN
@app.get("/redoc", response_class=HTMLResponse, include_in_schema=False)
async def redoc_html():
    """ReDoc documentation"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{settings.PROJECT_NAME} - ReDoc</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="icon" type="image/png" href="https://cdn.redoc.ly/redoc/logo-mini.svg">
        <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
        <style>
            body {{
                margin: 0;
                padding: 0;
            }}
        </style>
    </head>
    <body>
        <redoc spec-url="/openapi.json"></redoc>
        <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
    </body>
    </html>
    """

# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response