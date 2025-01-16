class Game:
    size = (960, 540)
    def __init__(self, name:str, location:tuple) -> None:
        self.name = name
        self.location = location
    def __str__(self) -> str: return f"{self.name} at {self.location}"