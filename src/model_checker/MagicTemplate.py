import base64
import pickle
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

    def serialize(self) -> str:
        return str(base64.b64encode(pickle.dumps(self)), encoding='utf-8')

    # @abstractmethod
    # def initial_state(self) -> List[State] or List[Iterable]:
    #     """
    #     初始化所有状态
    #     """
    #     raise NotImplementedError()
    #
    # @abstractmethod
    # def initial_event(self) -> List[Event] or List[Iterable]:
    #     """
    #     初始化所有事件
    #     """
    #     raise NotImplementedError()
    #
    # @abstractmethod
    # def initial_variable(self) -> dict:
    #     """
    #     定义模型相关的变量，最好不要直接在self直接定义变量。因为模型检测的时候不会复制self中的变量
    #     :return:
    #     """
    #     raise NotImplementedError()


def deserialize(data: str) -> MagicTemplate:
    return pickle.loads(base64.b64decode(data))
