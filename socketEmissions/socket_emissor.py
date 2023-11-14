import datetime
import uuid

from flask_socketio import SocketIO

from app import pending_messages, attempt_send_message


def pulseEmit(socketInstance: SocketIO, data: dict):
    socketInstance.emit('message', data)
    print("Emitting data: ", data)
    return True


async def send_message(message):
    message_id = str(uuid.uuid4())
    message['id'] = message_id

    # Armazenar informações da mensagem
    pending_messages[message_id] = {
        'message': message,
        'timestamp': datetime.datetime.now(),
        'attempts': 0
    }

    # Enviar a mensagem e iniciar o processo de verificação
    await attempt_send_message(message_id)
