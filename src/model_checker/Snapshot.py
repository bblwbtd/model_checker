from src.model_checker.State import State


class Snapshot:
    def __init__(self, state: State, values: dict):
        self.values = values
        self.state = state
