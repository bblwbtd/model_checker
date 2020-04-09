from typing import Iterable

from src.model_checker.Event import Event
from src.model_checker.State import State


class FiniteStateMachine:

    def __init__(self, events: Iterable[Event], states: Iterable[State]):

        self.__event_map = {
            event.name: event
            for event in events
        }
        self.__state_map = {
            state.name: state
            for state in states
        }
        self.__construct_machine()

        for state in states:
            if state.is_initial:
                self.current_state = state

    def __construct_machine(self):
        for i in self.__event_map:
            event = self.__event_map[i]
            src = self.__state_map[event.src]
            des = self.__state_map[event.des]
            src.add_outbound(event)
            des.add_inbound(event)

    def get_possible_next_event(self):
        return self.current_state.outbound

    def is_final(self) -> bool:
        return self.current_state.is_final

    def trigger_event(self, event: str or Event, model):
        if type(event) == str:
            event = self.__event_map[event]
        if event.name not in self.current_state.outbound:
            raise Exception(f"Can not incur {event.name}")
        self.current_state.on_leave_state(model)
        self.current_state = self.__state_map[event.des]
        event.on_event(model)
        self.current_state.on_enter_state(model)

    def get_state(self, name: str) -> State:
        return self.__state_map[name]

    def get_event(self, name: str) -> State:
        return self.__event_map[name]

    def set_state(self, state: str or State):
        if type(state) is str:
            self.current_state = self.__state_map[state]
        else:
            self.current_state = state
