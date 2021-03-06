from nthuee_prautogen.rpautogen import ReportManager
import sys
import json

VAR_FILE = "var.json"
DATA_FILE = "data.csv" if len(sys.argv) < 2 else sys.argv[1]

with open(VAR_FILE, "r") as f:
    usrvar = json.load(f)

rpmng = ReportManager(usrvar)
if rpmng.connect_server():
    with open(DATA_FILE, "r") as f:
    	if rpmng.submit_progress(csvfile=f):
    		print "Submit Success!"

rpmng.finalize()
