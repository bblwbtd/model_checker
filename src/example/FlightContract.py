from typing import List, Iterable

from src.model_checker import *

insurance_price = 10
compensation = 1000


class FlightContractValidator(Validator):
    def validate(self, model: MagicModel):
        if model.fsm.is_final():
            values = model.values
            correct_case = [
                {
                    'a': 0,
                    'b': 0,
                    's': 0
                },
                {
                    'a': insurance_price - compensation,
                    'b': compensation - insurance_price,
                    's': 0,
                },
                {
                    'a': insurance_price,
                    'b': -insurance_price,
                    's': 0
                }
            ]

            if values in correct_case:
                return True

            raise Exception("error detected!")


class FlightContractModel(MagicModel):

    def initial_variable(self) -> dict:
        return {
            'a': 0,
            'b': 0,
            's': 0
        }

    def initial_state(self) -> List[State] or List[Iterable]:
        return [
            State("c3bas,c4act,c5act,c6act,c7act,c8act", is_initial=True),
            State("c3vio, c4exp", is_final=True),
            State("c3sat, c4bas"),
            State("c4vio", is_final=True),
            State("c4sat, c5bas"),
            State("c5vio, c6bas"),
            State("v6sat", is_final=True),
            State("c5sat"),
            State("c7bas"),
            State("c8bas"),
            State("c7sat", is_final=True),
            State("c8sat", is_final=True)
        ]

    def initial_event(self) -> List[Event] or List[Iterable]:
        return [
            Event("timeout1", "c3bas,c4act,c5act,c6act,c7act,c8act", "c3vio, c4exp", ),
            Event("buy_ticket", "c3bas,c4act,c5act,c6act,c7act,c8act", "c3sat, c4bas"),
            Event("timeout2", "c3sat, c4bas", "c4vio"),
            Event("deposit(b,s,10)", "c3sat, c4bas", "c4sat, c5bas", self.transfer, ('b', 's', 10)),
            Event("timeout3", "c4sat, c5bas", "c5vio, c6bas"),
            Event("refund", "c5vio, c6bas", "v6sat", self.transfer, ('s', 'b', 10)),
            Event("deposit(a,s,1000)", "c4sat, c5bas", "c5sat", self.transfer, ('a', 's', 1000)),
            Event("flight_delay", "c5sat", "c7bas"),
            Event("on_time", "c5sat", "c8bas"),
            Event("transfer(s,a,1000), compensate(s, a, 1000)", "c8bas", "c8sat", self.on_finish1),
            Event("transfer(s,a,1000), compensate(s, b, 1000)", "c7bas", "c7sat", self.on_finish2)
        ]

    def transfer(self, src: str, des: str, value: int):
        self.values[src] = self.values[src] - value
        self.values[des] = self.values[des] + value

    def on_finish2(self):
        self.transfer('s', 'a', 10)
        self.transfer('s', 'b', 1000)

    def on_finish1(self):
        self.transfer('s', 'a', 10)
        self.transfer('s', 'a', 1000)


validator = FlightContractValidator()
test = FlightContractModel(validator)
test.dfs_check(1000)
