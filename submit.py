from rpautogen import ReportManager
import socket

if socket.gethostbyname(socket.gethostname()).startswith("140.114"):
	rpmng = ReportManager("var.json")
	if rpmng.connect_server():
		if rpmng.submit_progress("data.csv"):
			print "Submit Success!"
else:
	print "The IP is not under NTHU."
