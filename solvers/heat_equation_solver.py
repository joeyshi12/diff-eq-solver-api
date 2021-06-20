from typing import Dict

import numpy as np

from solvers.differential_equation_solver import DifferentialEquationSolver
from solvers.equation import HeatEquation, DifferentialEquationSolution, BoundaryCondition, Boundary
from solvers.exception import InvalidEquationError


class HeatEquationSolver(DifferentialEquationSolver):
    def parse_equation(self, params: Dict) -> HeatEquation:
        print('Parsing heat equation: %s' % str(params))
        try:
            alpha = float(params['alpha'])
            length = float(params['length'])
            time_period = float(params['time_period'])
            samples = int(params['samples'])
            left_condition = params['boundary']['left_condition']
            right_condition = params['boundary']['right_condition']
            boundary = Boundary(
                BoundaryCondition(left_condition['type'], lambda t: eval(left_condition['function'])),
                BoundaryCondition(right_condition['type'], lambda t: eval(right_condition['function']))
            )
            def initial_values(x: float) -> float: return eval(params['initial_condition'][0])
            return HeatEquation(alpha, length, time_period, samples, boundary, [initial_values])
        except(KeyError, ValueError, NameError):
            raise InvalidEquationError

    def solve(self, equation: HeatEquation) -> DifferentialEquationSolution:
        print('Solving: %s' % str(equation))
        dimensions = [(0, equation.time_period), (0, equation.length)]
        dx = equation.length / (equation.samples - 1)
        time_samples = 2 * int((2 * equation.alpha * equation.time_period) / (dx ** 2)) + 1
        dt = equation.time_period / (time_samples - 1)
        r = equation.alpha * dt / dx ** 2
        D = np.zeros((equation.samples - 2, equation.samples))
        for i in range(equation.samples - 2):
            D[i, i] = r
            D[i, i + 1] = 1 - 2 * r
            D[i, i + 2] = r

        # initialize solution array
        solution = np.zeros((time_samples, equation.samples))
        solution[0] = equation.initial_condition[0](np.arange(equation.samples) * dx)
        left_condition, right_condition = equation.boundary.left_condition, equation.boundary.right_condition

        # compute rest of solution values
        for k in range(1, time_samples):
            solution[k, 1:equation.samples - 1] = D @ solution[k - 1]
            solution[k, 0] = left_condition.function(k * dt) if left_condition.type == 'D' \
                else solution[k, 1] - left_condition.function(k * dt) * dx
            solution[k, -1] = right_condition.function(k * dt) if right_condition.type == 'D' \
                else solution[k, -2] + right_condition.function(k * dt) * dx
        return DifferentialEquationSolution(dimensions, solution.tolist())
