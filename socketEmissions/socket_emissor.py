import datetime
import uuid

from flask_socketio import SocketIO



def pulseEmit(socketInstance: SocketIO, data: dict):
    socketInstance.emit('message', data)
    print("Emitting data: ", data)
    return True



