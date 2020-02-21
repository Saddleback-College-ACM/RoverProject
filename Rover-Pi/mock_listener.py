import atexit
import threading
import logging
from io import BytesIO
from base64 import b64encode
from socketIO_client import SocketIO, BaseNamespace
from mock_i2c_backend import PyCar

KEY = b'0kXMZqwpoAgRUqOXk2Tjsubd1qndPyGR'
HOST = '192.168.1.87'
#HOST = 'muchomath.us.to'
PORT = 5000

logging.getLogger('socketIO-client').setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
car = PyCar()


@atexit.register
def neutralize():
    car.control(90, 90)

class RoverNamespace(BaseNamespace):
    def __init__(self, *args, **kwargs):
        BaseNamespace.__init__(self, *args, **kwargs)
        self.neutralize_timer = None
        self.start_neutralize_timer()

    def start_neutralize_timer(self):
        self.neutralize_timer = threading.Timer(1.0, neutralize)
        self.neutralize_timer.start()

    def on_connect(self):
        logger.info('connected')

    def on_reconnect(self):
        logger.info('reconnected')

    def on_disconnect(self):
        logger.info('disconnected')
        neutralize()

    def on_control(self, message):
        if self.neutralize_timer:
            self.neutralize_timer.cancel()
        steering = message.get('steering', 90)
        throttle = message.get('throttle', 90)
        try:
            car.control(steering, throttle)
        except:
            logger.error('Car connection dropped')
        self.start_neutralize_timer()

socketIO = SocketIO(HOST, PORT)
rover_namespace = socketIO.define(RoverNamespace, '/rover')

if __name__ == '__main__':
    socketIO.wait()

