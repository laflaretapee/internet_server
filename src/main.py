import aioredis as aioredis
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_users import FastAPIUsers

from src.auth.base_config import auth_backend
from src.auth.models import User
from src.auth.manager import get_user_manager
from src.auth.shemas import UserRead, UserCreate
from .operations.router import router as router_operations

app = FastAPI(
    title='Hackaton'
)
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_operations)


@app.on_event('startup')
async def startup_event():
    redis = aioredis.from_url('redis://localhost', encoding='utf-8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
