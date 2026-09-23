from abc import ABC, abstractmethod
from dataclasses import dataclass
from pythonscad import cube

from pyscad.sign_gen.parameters import BaseParameters

class SignShape(ABC):
    """
    Base class for shape of sign
    """
    def __init__(
            self,
            params: BaseParameters = BaseParameters()
    ):
        self.params = params

    def build(self):
        self.build_base()
        self.build_border()

    @abstractmethod
    def build_base(self) -> object:
        """
        Returns a pythonscad shape containing the base sign, centered
        """
        raise NotImplementedError()

    @abstractmethod
    def build_border(self) -> object:
        """
        Returns the raised sign border as a separate object
        """
        raise NotImplementedError()