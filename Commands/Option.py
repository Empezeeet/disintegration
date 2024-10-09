from dataclasses import dataclass, asdict


@dataclass
class Option:
    type: int
    name: str # 1-32
    description: str
    required: bool
    def __post_init__(self):
        if self.required is None:
            self.required = False
    def dict(self):
        return {k: v for k,v in asdict(self).items()}