from rpautogen import ReportManager

rpmng = ReportManager("var.json")
if rpmng.connect_server():
	if rpmng.submit_progress("data.csv"):
		print "Submit Success!"
