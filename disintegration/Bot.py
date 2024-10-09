from disintegration.Commands import SlashCommand


class Bot:
    def __init__(self, token, appid, activityName: str,commands: dict[str, SlashCommand] = None):
        self._token = token
        self.appid = appid
        self.activityName = activityName
        if commands is None:
            self.commands = {}
        else:
            self.commands = commands

    def getToken(self) -> str:
        return self._token
    def get_command(self, name: str):
        command = self.commands.get(name, None)
        if command is None:
            raise TypeError
        else:
            return command