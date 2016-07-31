from rpautogen import ReportManager
import sys

VAR_FILE = "var.json"
DATA_FILE = "data.csv" if len(sys.argv) < 2 else sys.argv[1]

rpmng = ReportManager(VAR_FILE)
if rpmng.connect_server():
	if rpmng.submit_progress(DATA_FILE):
		print "Submit Success!"
