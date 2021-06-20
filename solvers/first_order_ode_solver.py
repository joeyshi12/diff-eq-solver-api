import numpy as np
from typing import Dict

from solvers.differential_equation_solver import DifferentialEquationSolver
from solvers.equation import FirstOrderODE, DifferentialEquationSolution
from solvers.exception import InvalidEquationError


class FirstOrderODESolver(DifferentialEquationSolver):
    def parse_equation(self, params: Dict) -> FirstOrderODE:
        print('Parsing first order ODE: %s' % str(params))
        try:
            samples = int(params['samples'])
            time_period = float(params['time_period'])
            initial_value = float(params['initial_value'])
            def source(t: float, x: float) -> float: return eval(params['source'])
            return FirstOrderODE(samples, time_period, initial_value, source)
        except(KeyError, ValueError, NameError):
            raise InvalidEquationError

    def solve(self, equation: FirstOrderODE) -> DifferentialEquationSolution:
        print('Solving: %s' % str(equation))
        dimensions = [(0, equation.time_period)]
        solution = np.zeros(equation.samples)
        solution[0] = equation.initial_value
        dt = equation.time_period / (equation.samples - 1)
        for i in range(1, equation.samples):
            solution[i] = solution[i - 1] + equation.source(i * dt, solution[i - 1]) * dt
        return DifferentialEquationSolution(dimensions, list(solution))
