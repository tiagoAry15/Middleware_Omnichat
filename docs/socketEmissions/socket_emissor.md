## _socket_emissor.py_
This module is responsible for emitting data pulses to the frontend through webhooks. It utilizes Flask-SocketIO to facilitate real-time communication between the server and the frontend. Here are the functionalities it provides:

- **pulseEmit**: A function that takes a SocketIO instance and a data dictionary as inputs, and emits the data as a message to the frontend. It also logs the emitted data to the console.

### Usage:

```python
from flask_socketio import SocketIO
from socket_emissor import pulseEmit

# Initialize SocketIO instance
socketio = SocketIO(app)

# Data to be emitted
data = {"message": "Hello, World!"}

# Emit data pulse
pulseEmit(socketio, data)
```