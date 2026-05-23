from fastapi_mail import MessageSchema, MessageType
from app.core.mail import mail

async def send_order_created_email(
    responsible_email: str,
    responsible_name: str,
    order_title: str,
    order_id: int,
):
    message = MessageSchema(
        subject=f"Nova ordem de serviço atribuída: {order_title}",
        recipients=[responsible_email],
        body=f"""
        Olá, {responsible_name}!

        Uma nova ordem de serviço foi atribuída a você.

        ID: {order_id}
        Título: {order_title}

        Acesse o sistema para mais detalhes.
        """,
        subtype=MessageType.plain,
    )
    await mail.send_message(message)

async def send_status_changed_email(
    responsible_email: str,
    responsible_name: str,
    order_title: str,
    order_id: int,
    old_status: str,
    new_status: str,
):
    message = MessageSchema(
        subject=f"Status atualizado: {order_title}",
        recipients=[responsible_email],
        body=f"""
        Olá, {responsible_name}!

        O status da ordem de serviço foi atualizado.

        ID: {order_id}
        Título: {order_title}
        Status anterior: {old_status}
        Novo status: {new_status}
        """,
        subtype=MessageType.plain,
    )
    await mail.send_message(message)

async def send_order_canceled_email(
    client_email: str,
    client_name: str,
    order_title: str,
    order_id: int,
):
    message = MessageSchema(
        subject=f"Ordem de serviço cancelada: {order_title}",
        recipients=[client_email],
        body=f"""
        Olá, {client_name}!

        Sua ordem de serviço foi cancelada.

        ID: {order_id}
        Título: {order_title}

        Entre em contato para mais informações.
        """,
        subtype=MessageType.plain,
    )
    await mail.send_message(message)