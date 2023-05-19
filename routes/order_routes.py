from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from models.models import User, Order
from schemas.order_schemas import OrderModel
from db.database import Session, engine
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()
session = Session(bind=engine)

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
            "message": f"Order {new_order.id} placed successfuly"
        }
    )

@router.get("/orders")
async def list_all_router(Authorize:AuthJWT = Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    
    current_user = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff == True:
        orders = session.query(Order).all()
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content={
                "orders": jsonable_encoder(orders)
            }
        )
    return JSONResponse(
            status_code = status.HTTP_403_FORBIDDEN,
            content={
                "message": "User is not superuser" 
            }
    )
@router.get("/orders/{order_id}")
async def get_order_by_id(order_id:int,Authorize:AuthJWT=Depends()):

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    user=Authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==user).first()

    if current_user.is_staff:
        order=session.query(Order).filter(Order.id==order_id).first()

        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content={
                "order": jsonable_encoder(order)
            }
        )

    return JSONResponse(
            status_code = status.HTTP_403_FORBIDDEN,
            content={
                "message": "User is not superuser" 
            }
    )

@router.get('/user/orders')
async def get_user_orders(Authorize:AuthJWT=Depends()):

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    user=Authorize.get_jwt_subject()


    current_user=session.query(User).filter(User.username==user).first()

    return JSONResponse(
            status_code = status.HTTP_200_OK,
            content={
                "order": jsonable_encoder(current_user.orders)
            }
        )

@router.get('/user/order/{order_id}/')
async def get_specific_order(order_id:int,Authorize:AuthJWT=Depends()):

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    user=Authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==user).first()

    orders=current_user.orders

    for order in orders:
        if order.id == order_id:
            return JSONResponse(
            status_code = status.HTTP_200_OK,
            content={
                "order": jsonable_encoder(order)
            }
        )
    return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content={
                "message": "No order with such id" 
            }
    )