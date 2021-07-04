import numpy as np
from typing import Dict

from app.solvers.differential_equation_solver import DifferentialEquationSolver
from app.equation import SecondOrderODE, DifferentialEquationSolution
from app.exception import InvalidEquationError


class SecondOrderODESolver(DifferentialEquationSolver):
    def parse_equation(self, params: Dict) -> SecondOrderODE:
        print('Parsing: %s' % str(params))
        try:
            samples = int(params['samples'])
            time_period = float(params['time_period'])
            initial_value = float(params['initial_value'])
            initial_derivative = float(params['initial_derivative'])
            def source(t: float, x: float, y: float) -> float: return eval(params['source'])
            return SecondOrderODE(samples, time_period, initial_value, initial_derivative, source)
        except:
            raise InvalidEquationError

    def solve(self, equation: SecondOrderODE) -> DifferentialEquationSolution:
        print('Solving: %s' % str(equation))
        dimensions = [(0, equation.time_period)]
        solution = np.zeros(equation.samples)
        solution[0] = equation.initial_value
        derivative = equation.initial_derivative
        dt = equation.time_period / (equation.samples - 1)
        for i in range(1, equation.samples):
            solution[i] = solution[i - 1] + derivative * dt
            derivative = derivative + equation.source((i - 1) * dt, solution[i - 1], derivative) * dt
        return DifferentialEquationSolution(dimensions, list(solution))
