import socketio
import random
import time
import schedule
import signal
import sys


def signal_handler(sig, frame):
    print("\rExiting...")
    socketio.disconnect()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

socketio = socketio.Client()

socketio.connect("http://localhost:5000")


def send_data():
    socketio.emit('mqtt-data', random.randint(1, 100))


schedule.every().seconds.do(send_data)

while True:
    schedule.run_pending()
    time.sleep(1)
