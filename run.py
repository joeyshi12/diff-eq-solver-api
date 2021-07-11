import io
from random import random
from uuid import uuid4

from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Figure

from app.document_builder import DocumentBuilder
from app.solver_service import SolverService
from app.exception import InvalidEquationError

app = Flask(__name__)
CORS(app)
solver_service = SolverService(app)


@app.route("/solve/<type>", methods=["POST"])
def solve_equation(type: str):
    data = request.get_json()
    if data is None:
        return jsonify({"message": "no data was received in request"}), 500
    try:
        equation_id = str(uuid4())
        solver_service.solve_and_store(data, type, equation_id)
        return jsonify({"status": "running", "id": equation_id}), 200
    except InvalidEquationError:
        return jsonify({"message": "invalid equation"}), 200


@app.route("/solutions/status/<id>", methods=["GET"])
def get_solution_status_by_id(id: str):
    return jsonify({"status": solver_service.check_status(id), "id": id}), 200


@app.route("/solutions/export/<id>", methods=["GET"])
def export_solution_by_id(id: str):
    solution = solver_service.get_solution(id)
    document = DocumentBuilder.build(solution)
    filename = "{id}.xlsx".format(id=id)
    return send_file(document, attachment_filename=filename, as_attachment=True)


@app.route("/solutions/plot/<id>", methods=["GET"])
def get_plot_by_id(id: str):
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
