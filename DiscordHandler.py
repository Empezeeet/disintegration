import threading

import requests
import websocket
import json

from disintegration.acketFactory import PacketFactory
from disintegration.Logger import Logger, LogType
from disintegration.Bot import Bot
from disintegration.HeartbeatManager import HeartbeatManager
from disintegration.Commands.SlashCommand import SlashCommand

class DiscordHandler:



    def __init__(self, bot: Bot):

        self._websocket: websocket.WebSocket = websocket.WebSocket()
        self._bot: Bot = bot
        self._logger: Logger = Logger("DiscordHandler")

        self._lastSequence = None
        self.event: str = ""
        self.heartbeatIntervalMilliseconds: int = 0
        self.sessionID = ""
        self.resumeURL = ""



        self._logger.print("Initializing DiscordHandler")
        # Connect to Discord and receive Hello Event
        self._connectToGateway()
        # Start heart beating thread.
        self._startHeartbeat(self.heartbeatIntervalMilliseconds)
        # Send Identify
        self._identify()

        # Upload Commands.
        self._setupCommands()

        threading.Thread(self._autohandler())


        # Start autohandler loop.
    def _handleCommand(self, response: dict):
        command_data: dict = response.get("d")
        command_name: str = command_data.get('data').get("name")
        command_func: SlashCommand = self._bot.get_command(command_name)

        if command_func:
            self._logger.print(f"Executing command {command_name}")
            command_func.on_use(command_data.get("token"), command_data.get("id"), self._bot.getToken())
        else:
            self._logger.print(f"Command {command_name} not found")



    def _autohandler(self):
        while True:
            packet: dict = self.receiveResponse()
            # try to auto handle response
            # if handler couldn't handle
            self.handleResponse(packet)

    # loads commands and sends them off to discord
    def _setupCommands(self):
        url: str = f"https://discord.com/api/v10/applications/{self._bot.appid}/commands"
        headers: dict = {"Authorization": f"Bot {self._bot.getToken()}"}
        command: SlashCommand
        name: str
        for name, command in self._bot.commands.items():
            r = requests.post(url, headers=headers, json=command.setupPacket)
            self._logger.print(f"Loaded Command {command.name} with status: {r.status_code}\n {r.json()}")
    # function handles identifying and receiving Ready event.
    def _identify(self):
        self._logger.print("[Identify] Sent Identify Packet")
        self._websocket.send(json.dumps(PacketFactory.identifyPacket(self._bot.getToken(), self._lastSequence, self._bot.activityName)))
        # Receive READY event
        self._logger.print("[Identify] Receiving READY event")
        self.handleResponse()

    def _startHeartbeat(self, intervalMilliseconds: int):
        self._heartBeatManager: HeartbeatManager = HeartbeatManager(intervalMilliseconds, self._websocket, self._logger)

    # function handles connecting to gateway and receiving Hello Packet.
    def _connectToGateway(self):
        self._logger.print("Connecting to Discord's Gateway")
        self._websocket.connect('wss://gateway.discord.gg/?v=6&encoding=json')

        if not self.handleResponse()[0]:
            self._logger.print("[eventConnect To Gateway] Error occurred when handling Hello Event", logType=LogType.ERROR)
            breakpoint()
        self._logger.print("[Connect To Gateway] Successfully connected to Discord's Gateway")

    # Returns TRUE if response was handled automatically
    # Returns FALSE if program couldn't handle response.
    def handleResponse(self, response: dict = None) -> [bool, dict]:
        if response is None:
            response: dict = self.receiveResponse()
        match response.get('op', -1):
            case -1:
                # program occurred error so return false
                self._logger.print(f"[Handler Error] Couldn't auto-handle response!\n Response:\n{response}\n----")
                breakpoint()
                return [False, response]
            case 7:
                # TODO OP 07
                self._logger.print(f"[Handler] Gateway requested connection resume")
                self._websocket.connect('wss://gateway.discord.gg/?v=6&encoding=json')
                self._websocket.send(
                    json.dumps(
                        PacketFactory.resumePacket(self._bot.getToken(), self.sessionID, self._lastSequence)
                    )
                )
                raise NotImplementedError()
            case 10:
                self._logger.print("Received HELLO event.")
                # Hello Event
                try:
                    self.heartbeatIntervalMilliseconds = response.get("d").get("heartbeat_interval")
                    return [True, {}]
                except AttributeError as e:
                    self._logger.print("mad error! report to github with .botlog file\n" + str(e))
                    breakpoint()
                    return [False, response]
            case 11:
                self._logger.print("Heartbeat received")
                return [True, {}]
        if response.get("op") != 0:
            self._logger.print("Unhandled packet!", logType=LogType.ERROR)
            self._logger.print("PACKET: " + str(response))
            raise NotImplementedError()


        match response.get("t"):
            case "READY":
                self._logger.print("Received READY event.")
                # Ready event
                try:
                    self.sessionID = response.get("d").get("session_id")
                    self.resumeURL = response.get("d").get("resume_url")
                except AttributeError as e:
                    self._logger.print("mad error! report to github with .botlog file\n" + str(e))
                    breakpoint()
                    return [False, response]
                self._logger.print("Sucessfully parsed READY event")
                return [True, {}]
            case "INTERACTION_CREATE":
                self._logger.print("Received INTERACTION_CREATE event.")
                self._handleCommand(response)
        return [True, {}]



    def receiveResponse(self) -> dict:
        response = None
        while True:
            try:
                response = self._websocket.recv()
                break
            except websocket.WebSocketConnectionClosedException as e:
                self._logger.print("[Gateway] Connection closed")
                self._logger.print(f"An error occurred!\n {e}")
                self._websocket.close()
                exit()
            except KeyboardInterrupt as e:
                self._logger.print("[Gateway] Closing Gateway on Keyboard Interrupt! " + str(e))
                # try handle this shit!

        self._lastSequence = json.loads(response)['s']
        self._logger.print(json.loads(response), logType=LogType.DEBUG)
        return json.loads(response)




