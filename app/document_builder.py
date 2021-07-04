from io import BytesIO

from numpy import linspace
from pandas import DataFrame, ExcelWriter

from app.equation import DifferentialEquationSolution


class DocumentBuilder:
    @classmethod
    def build(cls, solution: DifferentialEquationSolution) -> BytesIO:
        num_dimensions = len(solution.dimensions)
        if num_dimensions == 1:
            start, end = solution.dimensions[0]
            time_samples = len(solution.solution)
            data_frame = DataFrame(
                solution.solution,
                columns=linspace(start, end, time_samples)
            )
            document = BytesIO()
            writer = ExcelWriter(document, engine='xlsxwriter')
            data_frame.to_excel(writer, sheet_name="Solution")
            writer.close()
            document.seek(0)
            return document
        elif num_dimensions == 2:
            index_start, index_end = solution.dimensions[0]
            column_start, column_end = solution.dimensions[1]
            position_samples = len(solution.solution[0])
            time_samples = len(solution.solution)
            data_frame = DataFrame(
                solution.solution,
                index=linspace(index_start, index_end, time_samples),
                columns=linspace(column_start, column_end, position_samples)
            )
            document = BytesIO()
            writer = ExcelWriter(document, engine='xlsxwriter')
            data_frame.to_excel(writer, sheet_name="Solution")
            writer.close()
            document.seek(0)
            return document
        else:
            raise Exception
