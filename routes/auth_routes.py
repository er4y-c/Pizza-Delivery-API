from fastapi import APIRouter, Depends
from db.database import Session, engine
from schemas.auth_schemas import SignUpModel, LoginModel
from models.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from starlette import status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from dynaconf import settings

router = APIRouter()
session = Session(bind=engine)

authjwt_secret_key = settings.get("auth.authjwt_secret_key")

AuthJWT.secret_key = authjwt_secret_key

@router.get("/")
async def hello():
    return {"message":"Hello world"}

@router.post("/signup")
async def signup(user:SignUpModel):
    registered_email = session.query(User).filter(User.email==user.email).first()

    if registered_email is not None:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "status_code": status.HTTP_409_CONFLICT,
                "error": "User with the email already exists"
            }
        )

    registered_username =session.query(User).filter(User.username==user.username).first()

    if registered_username is not None:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "status_code": status.HTTP_409_CONFLICT,
                "error": "User with the email already exists"
            }
        )

    new_user=User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )

    session.add(new_user)

    session.commit()

    return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": f"{new_user.username} is created."
            }
        )

@router.post("/login")
async def login(user:LoginModel, Authorize:AuthJWT = Depends()):
    db_user = session.query(User).filter(User.username == user.username).first()
    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)
        
        response = {
          "access_token": access_token,
          "refresh_token": refresh_token
        }
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                jsonable_encoder(response)
            }
        )
    
    return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "message": "Invalid username or password"
            }
        )