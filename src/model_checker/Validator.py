from abc import abstractmethod


class Validator:
    @abstractmethod
    def validate(self, model):
        """
        检测模型状态是否符合预期，如果出现问题直接抛出异常否则直接返回
        :param model: 所检测的模型
        :return: None
        """
        raise NotImplementedError()
