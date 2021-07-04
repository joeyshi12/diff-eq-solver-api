from abc import abstractmethod, ABC
from typing import Dict

from app.equation import DifferentialEquation, DifferentialEquationSolution


class DifferentialEquationSolver(ABC):
    @abstractmethod
    def parse_equation(self, params: Dict) -> DifferentialEquation:
        raise NotImplementedError

    @abstractmethod
    def solve(self, equation: DifferentialEquation) -> DifferentialEquationSolution:
        raise NotImplementedError
