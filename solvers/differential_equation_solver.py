from abc import abstractmethod

from solvers.equation import DifferentialEquation, DifferentialEquationSolution


class DifferentialEquationSolver:
    @abstractmethod
    def parse_equation(self, params: object) -> DifferentialEquation:
        raise NotImplementedError

    @abstractmethod
    def solve(self, equation: DifferentialEquation) -> DifferentialEquationSolution:
        raise NotImplementedError
