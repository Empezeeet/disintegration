from abc import abstractmethod
from disintegration.Commands import Option

class SlashCommand:
    def __init__(self, name: str, description: str, options: list[Option] = None):
        if options is None:
            options = []
        self.name = name.lower()
        self.description = description
        self.setupPacket = {
            "name":name.lower(),
            "type":1,
            "description":description,
            "options": [option.dict() for option in options]
        }
        print(self.setupPacket)
    @staticmethod
    @abstractmethod
    def on_use(interactionToken: str, interactionID: str, token:str):
        pass
