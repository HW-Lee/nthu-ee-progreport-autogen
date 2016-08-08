import os
import json
import csv

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
    try:
        usrvar = {
            "vpn-username": request.form["vpn-username"],
            "vpn-userpwd": request.form["vpn-userpwd"],
            "username": request.form["username"],
            "userpwd": request.form["userpwd"],
            "studentname": request.form["studentname"]
        }

        data = {
            "thisweek": request.form["thisweek"].encode("big5"),
            "nextweek": request.form["nextweek"].encode("big5"),
            "deadline": request.form["deadline"].encode("big5"),
            "note": "submitted by ReportManager."
        }

    except:
        return make_response("key-missing", 200)

    resp = { "server-connected": False, "data-posted": False, "err-occur": False }
    rpmng = ReportManager(usrvar)
    try:
        if rpmng.connect_server(): 
            resp["server-connected"] = True
            if rpmng.submit_data(data): resp["data-posted"] = True

    except:
        resp["err-occur"] = True

    rpmng.finalize()

    return make_response(jsonify(resp), 200)

@app.route("/api/post/file", methods=["POST"], strict_slashes=False)
def post_file():
    if "var.json" in request.files.keys():
        usrvar = json.load(request.files["var.json"])
    else:
        return make_response("no var.json", 200)

    if "data.csv" in request.files.keys():
        csvfile = request.files["data.csv"]

        resp = { "server-connected": False, "data-posted": False, "err-occur": False }
        rpmng = ReportManager(usrvar)
        try:
            if rpmng.connect_server(): 
                resp["server-connected"] = True
                if rpmng.submit_progress(csvfile=csvfile): resp["data-posted"] = True

        except:
            resp["err-occur"] = True

        rpmng.finalize()

        return make_response(jsonify(resp), 200)
        
    else:
        return make_response("no data.csv", 200)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
