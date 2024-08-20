import abc


class UcitatiService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def identifier(self):
        pass

    @abc.abstractmethod
    def ucitati(self):
        pass