from abc import abstractmethod
from copy import deepcopy
from typing import List, Iterable

from .Event import Event
from .FiniteStateMachine import FiniteStateMachine
from .Snapshot import Snapshot
from .State import State
from .Validator import Validator


class MagicModel:
    def __init__(self, validator: Validator):
        self.validator = validator
        self.fsm = FiniteStateMachine(self.initial_event(), self.initial_state())
        self.values = self.initial_variable()

    def dfs_check(self, max_depth: int):
        history = [self.fsm.current_state]
        self.__dfs_step(max_depth, history)

    def __restore(self, snapshot: Snapshot):
        self.values = snapshot.values
        self.fsm.current_state = snapshot.state

    def __dfs_step(self, max_depth: int, history: list):
        if len(history) >= max_depth or self.fsm.is_final():
            return

        save = self.__take_snapshot()
        history.append(self.fsm.current_state)
        for event in self.fsm.current_state.outbound.values():
            self.fsm.trigger_event(event)
            try:
                self.validator.validate(self)
            except Exception as e:
                print(e)
                print(f'current values:{self.values}')
                continue
            copy_history = history[:]
            copy_history.append(event)
            self.__dfs_step(max_depth, copy_history)
            self.__restore(save)

    def __take_snapshot(self):
        return Snapshot(self.fsm.current_state, deepcopy(self.values))

    @abstractmethod
    def initial_state(self) -> List[State] or List[Iterable]:
        raise NotImplementedError()

    @abstractmethod
    def initial_event(self) -> List[Event] or List[Iterable]:
        raise NotImplementedError()

    @abstractmethod
    def initial_variable(self) -> dict:
        raise NotImplementedError()