from copy import deepcopy
from typing import Iterable

from .Event import Event
from .FiniteStateMachine import FiniteStateMachine
from .Snapshot import Snapshot
from .State import State


class MagicTemplate:
    def __init__(self, validator, variable: dict, states: Iterable[State], events: Iterable[Event]):
        self.variable = variable
        self.validator = validator
        self.fsm = FiniteStateMachine(events, states)

    def dfs_check(self, max_depth: int, variables: dict):
        history = [self.fsm.current_state]
        self.variable = variables
        self.__dfs_step(max_depth, history)

    def __restore(self, snapshot: Snapshot):
        self.variable = snapshot.values
        self.fsm.current_state = snapshot.state

    def __dfs_step(self, max_depth: int, history: list):
        if len(history) >= max_depth or self.fsm.is_final():
            return

        save = self.__take_snapshot()
        history.append(self.fsm.current_state)
        for event in self.fsm.current_state.outbound.values():
            self.fsm.trigger_event(event)
            try:
                self.validator.validate(self.variable)
            except Exception as e:
                print(e)
                print(f'current values:{self.variable}')
                continue
            copy_history = history[:]
            copy_history.append(event)
            self.__dfs_step(max_depth, copy_history)
            self.__restore(save)

    def __take_snapshot(self):
        return Snapshot(self.fsm.current_state, deepcopy(self.variable))


