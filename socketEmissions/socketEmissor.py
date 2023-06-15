from flask_socketio import SocketIO


def pulseEmit(socketInstance: SocketIO, data: dict):
    socketInstance.emit('message', data)
    return True
