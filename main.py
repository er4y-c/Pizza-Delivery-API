from fastapi import FastAPI
from routes.order_routes import router as order_routes
from routes.auth_routes import router as auth_routes
from fastapi_jwt_auth import AuthJWT
from schemas.auth_schemas import Settings

app = FastAPI()

@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(router=auth_routes, prefix="/auth", tags=["auth"])
app.include_router(router=order_routes, prefix="/order", tags=["order"])