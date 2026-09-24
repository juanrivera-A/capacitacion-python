from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...modulo01.models import Order, OrderItem, User
from ..dependencies import get_current_user, get_db
from ..schemas.auth import TokenData
from ..schemas.order import OrderCreate, OrderResponse

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_in: OrderCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[TokenData, Depends(get_current_user)],
):
    """Crea una nueva orden asociada a un usuario existente."""
    user = db.query(User).filter(User.id == order_in.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El usuario con ID {order_in.user_id} no existe",
        )

    new_order = Order(user_id=order_in.user_id, status="PENDING")
    db.add(new_order)
    db.flush()  # Asigna ID a la orden antes de insertar los ítems

    for item in order_in.items:
        new_item = OrderItem(
            order_id=new_order.id,
            product_name=item.product_name,
            quantity=item.quantity,
            price=item.price,
        )
        db.add(new_item)

    db.commit()
    db.refresh(new_order)
    return new_order


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[TokenData, Depends(get_current_user)],
):
    """Obtiene el detalle de una orden por su ID."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Orden con ID {order_id} no encontrada",
        )
    return order


@router.get("/", response_model=list[OrderResponse])
def list_orders(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[TokenData, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 10,
):
    """Lista las órdenes de la base de datos de forma paginada."""
    return db.query(Order).offset(skip).limit(limit).all()
