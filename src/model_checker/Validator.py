from abc import abstractmethod


class Validator:
    @abstractmethod
    def validate(self, model):
        raise NotImplementedError()
