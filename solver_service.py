from typing import Dict, List

from solvers.equation import DifferentialEquation, DifferentialEquationSolution
from solvers.exception import InvalidEquationTypeError, IdentifierCollisionError, MissingSolutionError
from solvers.first_order_ode_solver import FirstOrderODESolver
from solvers.heat_equation_solver import HeatEquationSolver
from solvers.second_order_ode_solver import SecondOrderODESolver
from solvers.wave_equation_solver import WaveEquationSolver


class SolverService:
    _solutions: Dict[str, DifferentialEquationSolution]
    _solvers: Dict[str, SecondOrderODESolver]

    def __init__(self):
        self._solutions = dict()
        self._solvers = dict(
            first_order_ode=FirstOrderODESolver(),
            second_order_ode=SecondOrderODESolver(),
            heat_equation=HeatEquationSolver(),
            wave_equation=WaveEquationSolver(),
        )

    def parse_equation(self, equation_type: str, data: Dict) -> DifferentialEquation:
        solver = self._solvers.get(equation_type, None)
        if solver is None:
            raise InvalidEquationTypeError
        return solver.parse_equation(data)

    def solve_and_store(self, equation_type: str, equation_id: str, equation: DifferentialEquation) -> None:
        solver = self._solvers.get(equation_type, None)
        if solver is None:
            raise InvalidEquationTypeError
        if equation_id in self._solutions:
            raise IdentifierCollisionError
        self._solutions[equation_id] = solver.solve(equation)

    def get_all_solutions(self) -> List[DifferentialEquationSolution]:
        return list(self._solutions.values())

    def get_by_id(self, equation_id: str) -> DifferentialEquationSolution:
        solution = self._solutions.get(equation_id, None)
        if solution is None:
            raise MissingSolutionError
        return solution
