from dataclasses import dataclass
from enum import Enum
from typing import List, Callable, Union, Tuple


@dataclass()
class FirstOrderODE:
    samples: int
    time_period: float
    initial_value: float
    source: Callable[[float, float], float]


@dataclass
class SecondOrderODE:
    samples: int
    time_period: float
    initial_value: float
    initial_derivative: float
    source: Callable[[float, float, float], float]


@dataclass
class BoundaryCondition:
    type: Enum('D', 'N')
    function: Callable[[float], float]


@dataclass
class Boundary:
    left_condition: BoundaryCondition
    right_condition: BoundaryCondition


@dataclass
class HeatEquation:
    alpha: float
    length: float
    time_period: float
    samples: int
    boundary: Boundary
    initial_condition: List[Callable[[float], float]]


@dataclass
class WaveEquation:
    c: float
    length: float
    time_period: float
    samples: int
    boundary: Boundary
    initial_condition: List[Callable[[float], float]]


@dataclass
class DifferentialEquationSolution:
    dimensions: List[Tuple[float, float]]
    solution: List


DifferentialEquation = Union[FirstOrderODE, SecondOrderODE, HeatEquation, WaveEquation]
