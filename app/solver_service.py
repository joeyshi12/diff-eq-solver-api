from typing import Dict

from flask import Flask
from flask_executor import Executor

from app.equation import DifferentialEquation, DifferentialEquationSolution
from app.exception import MissingSolutionError, CalculationNotDoneError, InvalidEquationError
from app.solvers.differential_equation_solver import DifferentialEquationSolver
from app.solvers.first_order_ode_solver import FirstOrderODESolver
from app.solvers.heat_equation_solver import HeatEquationSolver
from app.solvers.second_order_ode_solver import SecondOrderODESolver
from app.solvers.wave_equation_solver import WaveEquationSolver


class SolverService:
    _executor: Executor
    _solvers: Dict[str, DifferentialEquationSolver]

    def __init__(self, app: Flask):
        self._executor = Executor(app)
        self._solvers = dict(
            first_order_ode=FirstOrderODESolver(),
            second_order_ode=SecondOrderODESolver(),
            heat_equation=HeatEquationSolver(),
            wave_equation=WaveEquationSolver(),
        )

    def solve_and_store(self, data: Dict, equation_type: str, equation_id: str) -> None:
        solver = self._solvers.get(equation_type, None)
        if solver is None:
            raise InvalidEquationError
        equation = self._parse_equation(equation_type, data)
        self._executor.submit_stored(equation_id, solver.solve, equation)

    def check_status(self, equation_id: str) -> str:
        future_collection = self._executor.futures
        is_done = future_collection.done(equation_id)
        if is_done is None:
            return "failed"
        elif not is_done:
            return "running"
        else:
            return "success"

    def get_solution(self, equation_id: str) -> DifferentialEquationSolution:
        future_collection = self._executor.futures
        is_done = future_collection.done(equation_id)
        if is_done is None:
            raise MissingSolutionError
        elif not is_done:
            raise CalculationNotDoneError
        else:
            return future_collection.pop(equation_id).result()

    def _parse_equation(self, equation_type: str, data: Dict) -> DifferentialEquation:
        solver = self._solvers.get(equation_type, None)
        if solver is None:
            raise InvalidEquationError
        return solver.parse_equation(data)
