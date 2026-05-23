from app.core.database import SessionLocal

from app.services.user_service import register_user
from app.services.client_service import register_client
from app.services.service_order_service import create_service_order, change_service_order_status
from app.schemas.user import UserCreate
from app.schemas.client import ClientCreate
from app.schemas.service_order import ServiceOrderCreate
from app.utils.enums import ServiceOrderStatus
from app.repositories.user_repository import get_user_by_email
from app.repositories.client_repository import get_client_by_email
from app.repositories.service_order_repository import get_service_orders
from app.utils.enums import UserRole

db = SessionLocal()

try:
    existing_user = get_user_by_email(
        db=db,
        email="admin@example.com"
    )

    if not existing_user:
        user_data = UserCreate(
            name="Admin",
            email="admin@example.com",
            password="123456"
        )
        user = register_user(db, user_data)
        user.role = UserRole.ADMIN
        db.commit()
        print(f"Admin user created: {user.email}")
    else:
        user = existing_user
        print(f"Admin user already exists: {user.email}")

    existing_client1 = get_client_by_email(
        db=db,
        email="client1@example.com"
    )

    if not existing_client1:
        client1_data = ClientCreate(
            name="Client 1",
            email="client1@example.com",
            phone="+5511999999999"
        )
        client1 = register_client(db, client1_data)
        print(f"Client 1 created: {client1.email}")
    else:
        client1 = existing_client1
        print(f"Client 1 already exists: {client1.email}")

    existing_client2 = get_client_by_email(
        db=db,
        email="client2@example.com"
    )

    if not existing_client2:
        client2_data = ClientCreate(
            name="Client 2",
            email="client2@example.com",
            phone="+5511888888888"
        )
        client2 = register_client(db, client2_data)
        print(f"Client 2 created: {client2.email}")
    else:
        client2 = existing_client2
        print(f"Client 2 already exists: {client2.email}")

    existing_client3 = get_client_by_email(
        db=db,
        email="client3@example.com"
    )

    if not existing_client3:
        client3_data = ClientCreate(
            name="Client 3",
            email="client3@example.com",
            phone="+5511777777777"
        )
        client3 = register_client(db, client3_data)
        print(f"Client 3 created: {client3.email}")
    else:
        client3 = existing_client3
        print(f"Client 3 already exists: {client3.email}")

    existing_service_orders = get_service_orders(db)

    if not existing_service_orders:
        service_order1_data = ServiceOrderCreate(
            title="Service Order 1",
            description="Description for Service Order 1",
            priority="low",
            client_id=client1.id,
            responsible_user_id=user.id,
        )
        service_order1 = create_service_order(db, service_order1_data)
        print(f"Service Order 1 created: {service_order1.title}")

        service_order2_data = ServiceOrderCreate(
            title="Service Order 2",
            description="Description for Service Order 2",
            priority="high",
            client_id=client2.id,
            responsible_user_id=user.id,
        )
        service_order2 = create_service_order(db, service_order2_data)
        print(f"Service Order 2 created: {service_order2.title}")

        service_order3_data = ServiceOrderCreate(
            title="Service Order 3",
            description="Description for Service Order 3",
            priority="high",
            client_id=client3.id,
            responsible_user_id=user.id,
        )
        service_order3 = create_service_order(db, service_order3_data)
        print(f"Service Order 3 created: {service_order3.title}")

        service_order4_data = ServiceOrderCreate(
            title="Service Order 4",
            description="Description for Service Order 4",
            priority="low",
            client_id=client1.id,
            responsible_user_id=user.id,
        )
        service_order4 = create_service_order(db, service_order4_data)
        print(f"Service Order 4 created: {service_order4.title}")

        service_order5_data = ServiceOrderCreate(
            title="Service Order 5",
            description="Description for Service Order 5",
            priority="medium",
            client_id=client1.id,
            responsible_user_id=user.id,
        )
        service_order5 = create_service_order(db, service_order5_data)
        print(f"Service Order 5 created: {service_order5.title}")

        change_service_order_status(
            db=db,
            service_order_id=service_order1.id,
            new_status=ServiceOrderStatus.IN_PROGRESS,
            current_user_id=user.id,
            note="Started working on the service order"
        )
        print(f"Service Order 1 status updated to in_progress")

        change_service_order_status(
            db=db,
            service_order_id=service_order2.id,
            new_status=ServiceOrderStatus.IN_PROGRESS,
            current_user_id=user.id,
            note="Iniciando atendimento"
        )
        print(f"Service Order 2 status updated to in_progress")

        change_service_order_status(
            db=db,
            service_order_id=service_order2.id,
            new_status=ServiceOrderStatus.DONE,
            current_user_id=user.id,
            note="Atendimento concluído"
        )
        print(f"Service Order 2 status updated to done")

        change_service_order_status(
            db=db,
            service_order_id=service_order3.id,
            new_status=ServiceOrderStatus.CANCELED,
        current_user_id=user.id,
            note="Cancelado pelo cliente"
        )
        print(f"Service Order 3 status updated to canceled")
    else:
        print(f"{len(existing_service_orders)} service orders already exist, skipping service order creation.")

except Exception as error:
    print(f"Erro ao executar seed: {error}")
    db.rollback()
finally:
    db.close()