import mechanize
import json
import csv
from datetime import date

class ReportManager(object):
    ROOTURL = "http://emgt.ee.nthu.edu.tw/"
    LOGINERR_CHR = "log in error"

    def __init__(self, filename):
        with open(filename, "r") as f:
            usrvar = json.load(f)

        self.usrname = usrvar["username"]
        self.usrpwd = usrvar["userpwd"]
        self.stuname = usrvar["studentname"]
        self.br = mechanize.Browser()
        self.br.set_handle_robots(False)

    def connect_server(self):
        self.br.open(ReportManager.ROOTURL + "index.html")
        self.br.select_form(nr=0)
        self.br["Username"] = self.usrname
        self.br["Password"] = self.usrpwd
        res = self.br.submit()

        return not ReportManager.LOGINERR_CHR in res.read().lower()

    def submit_progress(self, filename):
        try:
            with open(filename, "r") as f:
                data = list(csv.reader(f, delimiter=","))

            del data[0]
            data = map(lambda r: {
                "student": self.stuname.encode("big5"),
                "thisweek": r[0].decode("utf-8").encode("big5"),
                "nextweek": r[1].decode("utf-8").encode("big5"),
                "deadline": str(date(int(r[4]), int(r[2]), int(r[3]))),
                "note": "submitted by ReportManager."
            }, data)

        except:
            print "Error in reading the csv file, please check your file is a valid csv file."
            return False

        try:
            for d in data:
                self.br.open(ReportManager.ROOTURL + "stu_record/message_post.php")
                self.br.select_form(name="form1")
                for key in d.keys():
                    self.br[key] = d[key]
                res = self.br.submit()

                if not "adding success" in res.read().lower():
                    print "Error in submitting the data:"
                    print "\t" + "\t".join(d.values())
                    return False

            return True

        except:
            print "Error in submitting logs."
            return False


