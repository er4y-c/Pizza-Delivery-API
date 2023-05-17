from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from models.models import User,Order
from schemas.order_schemas import OrderModel
from db.database import Session, engine
from fastapi.responses import JSONResponse

router = APIRouter()
session = Session(bind=engine)

@router.get("/")
async def hello(Authorize:AuthJWT = Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    return {"message":"Hello World"}

@router.post("/new_order")
async def new_order(order:OrderModel, Authorize:AuthJWT = Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    new_order = Order(
        pizza_size=order.pizza_size,
        quantity= order.quantity
    )
    new_order.user = user
    
    session.add(new_order)
    session.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "order": new_order
        }
    )