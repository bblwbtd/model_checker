from src.model_checker.Event import Event


class State:

    def __init__(self, name: str, on_enter_state=None, on_leave_state=None, is_initial=False, is_final=False):

        self.is_final = is_final
        self.is_initial = is_initial
        self.name = name
        self._enter_state_callback = on_enter_state
        self._leave_state_callback = on_leave_state
        self.inbound = {}
        self.outbound = {}

    def on_enter_state(self):
        if self._enter_state_callback is not None:
            self._enter_state_callback()

    def on_leave_state(self):
        if self._leave_state_callback is not None:
            self._leave_state_callback()

    def add_inbound(self, event: Event):
        self.inbound[event.name] = event

    def add_outbound(self, event: Event):
        self.outbound[event.name] = event

    def __str__(self):
        return self.name
