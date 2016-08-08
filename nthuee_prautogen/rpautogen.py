import mechanize
import json
import csv
from datetime import date
import socket

class ReportManager(object):
    ROOTURL = "http://emgt.ee.nthu.edu.tw/"
    VPNURL = "https://sslvpn.twaren.net/nthu"
    VPNURL_LOGIN_SUCC = "https://sslvpn.twaren.net/dana/home/index.cgi"
    VPNURL_LOGOUT = "https://sslvpn.twaren.net/dana-na/auth/logout.cgi"
    VPN_PREFIX = "https://sslvpn.twaren.net/dana/home/launch.cgi?url="
    IP_NTHU_PREFIX = "140.114"
    LOGINERR_CHR = "log in error"
    SUCCESS_CHR = "adding success"

    def __init__(self, usrvar):
        if "vpn-username" in usrvar.keys() and "vpn-userpwd" in usrvar.keys():
            self.vpn = {"usr": usrvar["vpn-username"], "pwd": usrvar["vpn-userpwd"]}
        else:
            self.vpn = None
        self.rooturl = None
        self.usrname = usrvar["username"]
        self.usrpwd = usrvar["userpwd"]
        self.stuname = usrvar["studentname"]
        self.br = mechanize.Browser()
        self.br.set_handle_robots(False)

    def finalize(self):
        ip = socket.gethostbyname(socket.gethostname())
        if not ip.startswith(ReportManager.IP_NTHU_PREFIX):
            self.br.open(ReportManager.VPNURL_LOGOUT)

    def connect_server(self):
        if self.rooturl != None: return False
        self.rooturl = ReportManager.ROOTURL

        ip = socket.gethostbyname(socket.gethostname())
        if not ip.startswith(ReportManager.IP_NTHU_PREFIX):
            self.br.open(ReportManager.VPNURL)
            self.br.select_form(name="frmLogin")
            self.br["username"] = self.vpn["usr"]
            self.br["password"] = self.vpn["pwd"]
            self.br.submit()
            self.rooturl = ReportManager.VPN_PREFIX + self.rooturl

            # Checking if there is any unterminated process
            try: 
                self.br.select_form(name="frmConfirmation")
                res = self.br.submit(name="btnContinue")
            except: pass

        self.br.open(self.rooturl + "index.html")
        self.br.select_form(nr=0)
        self.br["Username"] = self.usrname
        self.br["Password"] = self.usrpwd
        res = self.br.submit()

        return not ReportManager.LOGINERR_CHR in res.read().lower()

    def submit_progress(self, filename):
        if self.rooturl == None: return False
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
                self.br.open(self.rooturl + "stu_record/message_post.php")
                self.br.select_form(name="form1")
                for key in d.keys():
                    self.br[key] = d[key]
                res = self.br.submit()

                if not ReportManager.SUCCESS_CHR in res.read().lower():
                    print "Error in submitting the data:"
                    print "\t" + "\t".join(d.values())
                    return False

            return True

        except:
            print "Error in submitting logs."
            return False

    def submit_data(self, data):
        try:
            data["student"] = self.stuname.encode("big5")
            self.br.open(self.rooturl + "stu_record/message_post.php")
            self.br.select_form(name="form1")
            for k, v in data.items(): self.br[k] = v
            res = self.br.submit()

            return ReportManager.SUCCESS_CHR in res.read().lower()

        except:
            return False
