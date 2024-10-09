import time


class PacketFactory:
    def __init__(self):
        print("Created Packet Factory.")
    @staticmethod
    def authorizationHeader(token: str) -> dict:
        return {
            "Authorization": f"Bot {token}"
        }
    @staticmethod
    def resumePacket(token: str, sessionID: str, sequence: int) -> dict:
        return {
            "op":6,
            "d": {
                "token": token,
                "session_id": sessionID,
                "seq": sequence
            }
        }
    @staticmethod
    def identifyPacket(token: str, last_sequence: str, activityName: str) -> dict:
        return {
            "op":2,
            "d": {
                "token": token,
                "intents": 513,
                "properties": {
                    "os":"linux",
                    "browser":"Safari",
                    "device":"BDB"
                },
                "presence": {
                    "since":time.time(),
                    "activities": [{
                        "name": activityName,
                        "type":2,
                        "url": "https://github.com/empezeeet"

                    }],
                    "status":"online",
                    "afk":False
                }
            },
            "s": last_sequence,
            "t":None
        }