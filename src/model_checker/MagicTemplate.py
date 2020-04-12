from copy import deepcopy
from typing import Iterable

from .Event import Event
from .FiniteStateMachine import FiniteStateMachine
from .Snapshot import Snapshot
from .State import State
from ..server.Parser import function_wrapper


class MagicTemplate:
    def __init__(self, validator, variables: dict, states: Iterable[State], events: Iterable[Event]):
        self.variables = variables
        self.validator = function_wrapper(validator)
        self.fsm = FiniteStateMachine(events, states)
        self.errors = []

    def dfs_check(self, max_depth: int):
        self.__dfs_step(max_depth, [])
        return self.errors

    def __restore(self, snapshot: Snapshot):
        self.variables = snapshot.values
        self.fsm.current_state = snapshot.state

    def __dfs_step(self, max_depth: int, history: list):
        if len(history) >= max_depth or self.fsm.is_final():
            return
        save = self.__take_snapshot()
        history.append(self.fsm.current_state)
        for event in self.fsm.current_state.outbound.values():
            self.fsm.trigger_event(event, self)
            try:
                self.validator(self)
            except Exception as e:
                self.errors.append({
                    'error': str(e),
                    'history': [str(state) for state in history]
                })
                continue
            copy_history = history[:]
            copy_history.append(event)
            self.__dfs_step(max_depth, copy_history)
            self.__restore(save)

    def __take_snapshot(self):
        return Snapshot(self.fsm.current_state, deepcopy(self.variables))
