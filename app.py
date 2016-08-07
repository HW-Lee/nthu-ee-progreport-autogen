import json

from flask import Flask, jsonify, abort, request, make_response, url_for

from nthuee_prautogen.rpautogen import ReportManager

app = Flask(__name__, static_url_path = "")

@app.route("/", methods=["GET"])
def get_root():
    return ""

@app.route("/api", methods=["GET"], strict_slashes=False)
def get_index():
    return make_response("This is the web-service implemented API of nthuee_prautogen.", 200)

@app.route("/api/post", methods=["POST"], strict_slashes=False)
def post_data():
    return make_response(jsonify(request.form), 200)

if __name__ == '__main__':
    app.run(debug=True)
