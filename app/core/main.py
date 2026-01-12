from fastapi import FastAPI
from app.note.routes import note_router
from contextlib import asynccontextmanager
from app.core.middleware import register_middleware
from app.core.errors import register_all_errors
from app.auth.router import auth_router
version = "v1"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("App starting up......")
    yield
    print("App shutting down......")



app = FastAPI(
    
    title="Note_Making_Application",
    description="A Rest API for a note making web service",
    version=version,
    lifespan=lifespan
)

register_middleware(app)
register_all_errors(app)


# Notes routes
app.include_router(
    note_router,
    prefix=f"/api/{version}/note",
    tags=["notes"]
)
app.include_router(
    auth_router,
    prefix=f"/api/{version}/auth",
    tags=["auth"]
)