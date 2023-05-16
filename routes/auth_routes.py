from fastapi import APIRouter
from db.database import Session, engine
from schemas.signup_schemas import SignUpModel
from models.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from starlette import status
from fastapi.responses import JSONResponse

router = APIRouter()
session = Session(bind=engine)

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


