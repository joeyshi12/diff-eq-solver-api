from typing import Dict

import numpy as np

from app.solvers.differential_equation_solver import DifferentialEquationSolver
from app.equation import WaveEquation, DifferentialEquationSolution, Boundary, BoundaryCondition, BoundaryType
from app.exception import InvalidEquationError


class WaveEquationSolver(DifferentialEquationSolver):
    def parse_equation(self, params: Dict) -> WaveEquation:
        print('Parsing: %s' % str(params))
        try:
            c = float(params['c'])
            length = float(params['length'])
            time_period = float(params['time_period'])
            samples = int(params['samples'])
            left_condition = params['boundary']['left_condition']
            right_condition = params['boundary']['right_condition']
            boundary = Boundary(
                BoundaryCondition(
                    BoundaryType[left_condition['type']],
                    lambda t: eval(left_condition['function'])
                ),
                BoundaryCondition(
                    BoundaryType[right_condition['type']],
                    lambda t: eval(right_condition['function'])
                )
            )
            def initial_values(x: float) -> float: return eval(params['initial_condition'][0])
            def initial_derivatives(x: float) -> float: return eval(params['initial_condition'][1])
            return WaveEquation(c, length, time_period, samples, boundary, [initial_values, initial_derivatives])
        except:
            raise InvalidEquationError

    def solve(self, equation: WaveEquation) -> DifferentialEquationSolution:
        print('Solving: %s' % str(equation))
        dimensions = [(0, equation.time_period), (0, equation.length)]
        dx = equation.length / (equation.samples - 1)
        time_samples = 2 * int((equation.c * equation.time_period) / dx) + 1
        dt = equation.time_period / (time_samples - 1)
        r = (equation.c * dt / dx) ** 2
        D = np.zeros((equation.samples - 2, equation.samples))
        for i in range(equation.samples - 2):
            D[i, i] = r
            D[i, i + 1] = 2 * (1 - r)
            D[i, i + 2] = r

        # initialize solution array
        solution = np.zeros((time_samples, equation.samples))
        solution[0] = equation.initial_condition[0](np.arange(equation.samples) * dx)
        solution[1, 1:equation.samples - 1] = 0.5 * D @ solution[0]
        solution[1, 1:equation.samples - 1] +=\
            dt ** 2 * equation.initial_condition[1](np.arange(1, equation.samples - 1) * dx)
        left_condition, right_condition = equation.boundary.left_condition, equation.boundary.right_condition
        solution[1, 0] = left_condition.function(dt) if left_condition.type == BoundaryType.dirichlet \
            else solution[1, 1] - left_condition.function(dt) * dx
        solution[1, -1] = right_condition.function(dt) if right_condition.type == BoundaryType.dirichlet \
            else solution[1, -2] + right_condition.function(dt) * dx

        # compute rest of solution values
        for k in range(1, time_samples):
            solution[k, 1:equation.samples - 1] = D @ solution[k - 1]
            solution[k, 0] = left_condition.function(k * dt) if left_condition.type == BoundaryType.dirichlet \
                else solution[k, 1] - left_condition.function(k * dt) * dx
            solution[k, -1] = right_condition.function(k * dt) if right_condition.type == BoundaryType.dirichlet \
                else solution[k, -2] + right_condition.function(k * dt) * dx
        return DifferentialEquationSolution(dimensions, solution.tolist())
