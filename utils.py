import config
import json, leveldb, time, smtplib, os, time
from email.mime.text import MIMEText


class Logger:
    def __init__(self):
        self.f = open('email.txt', 'w')
        self.warn_times = 0
        self.write_email_header()

    def __exit__(self):
        self.f.close()

    def write_email_header(self):
        self.f.write('To: ' + ', '.join(config.EMAIL) + '\n')
        self.f.write('Subject: bitrader notification' + '\n')
        self.f.write('From: bitrader' + '\n')
        self.f.flush()

    def write_email_msg(self, msg):
        self.f.write('\n' + msg + '\n')
        self.f.flush()

    def send_email(self, msg):
        self.write_email_msg(msg)
        p = os.popen('sendmail -t < email.txt', 'w')
        time.sleep(1) # for sending mail
        self.f.seek(0)
        self.f.truncate()
        self.write_email_header()
        self.warn_times = 0

    def log(self, msg):
        print(msg)

    def time_header(self):
        return time.strftime("%d %b %Y %H:%M:%S", time.localtime())

    def debug(self, msg):
        if config.DEBUG:
            msg = self.time_header() + ' [DEBUG]: ' + msg
            self.log(msg)

    def info(self, msg):
        msg = self.time_header() + ' [INFO]: ' + msg
        self.log(msg)
        self.send_email(msg)

    def warn(self, msg):
        msg = self.time_header() + ' [WARN]: ' + msg
        self.log(msg)
        if self.warn_times < 10:
            self.write_email_msg(msg)
            self.warn_times += 1
        else:
            self.send_email(msg)

    def error(self, msg):
        msg = self.time_header() + ' [ERROR]: ' + msg
        self.log(msg)
        self.send_email(msg)


logger = Logger()

def kv2mid(kv):
    mid = [int(float(price)) for price in kv[1].split('|')]
    mid = (mid[0] + mid[1]) / 2 if len(mid) > 1 else mid[0]
    return mid

def json2leveldb():
    with open(config.PRICE_FILE) as price_data:
        price_json = json.loads(price_data.read())
        db = leveldb.LevelDB(config.LEVEL_DB)
        for time_price_pair in price_json:
            timestamp = str(int(time_price_pair[0]) / 1000)
            price = str(time_price_pair[1])
            db.Put(timestamp, price)
