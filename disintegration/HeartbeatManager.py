import json
import threading
import time
import websocket

from disintegration.Logger import Logger


class HeartbeatManager:
    def __init__(self, intervalMiliseconds: int, wbs: websocket.WebSocket, logger: Logger):
        self.intervalMiliseconds = intervalMiliseconds
        self.logger = logger
        self.heartbeatPacket = {
            "op": 1,
            "d":"null"
        }
        self.websocket = wbs
        threading.Thread(target=self.heartbeat).start()
    def heartbeat(self):
        self.logger.print("[HBM] Heartbeat loop activated.")
        self.websocket.send(json.dumps(self.heartbeatPacket))
        while True:
            time.sleep(self.intervalMiliseconds/1000)
            self.websocket.send(json.dumps(self.heartbeatPacket))
            self.logger.print("Sent heartbeat.")




