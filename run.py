from uuid import uuid4

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from app.document_builder import DocumentBuilder
from app.solver_service import SolverService
from app.exception import InvalidEquationError, MissingSolutionError, CalculationNotDoneError

app = Flask(__name__)
CORS(app)
solver_service = SolverService(app)


@app.route('/solve/<type>', methods=['POST'])
def solve_equation(type: str):
    data = request.get_json()
    if data is None:
        return jsonify({'message': 'no data was received in request'}), 500
    try:
        equation_id = str(uuid4())
        solver_service.solve_and_store(data, type, equation_id)
        return jsonify({'state': 'running', 'id': equation_id}), 200
    except InvalidEquationError:
        return jsonify({'message': 'invalid equation'}), 500


@app.route('/solutions/<id>', methods=['GET'])
def get_solution_by_id(id: str):
    try:
        solution = solver_service.get_by_id(id)
        return jsonify({'state': 'success', 'id': id, 'result': solution}), 200
    except MissingSolutionError:
        return jsonify({'message': 'solution %s does not exist' % id}), 500
    except CalculationNotDoneError:
        return jsonify({'state': 'running', 'id': id}), 200


@app.route('/solutions/<id>/export', methods=['GET'])
def export_solution_by_id(id: str):
    solution = solver_service.get_by_id(id)
    document = DocumentBuilder.build(solution)
    filename = "{id}.xlsx".format(id=id)
    return send_file(document, attachment_filename=filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
