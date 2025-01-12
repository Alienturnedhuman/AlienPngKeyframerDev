from flask import Flask
import os

app = Flask(__name__)

RECORD_PATH = "../"

@app.route('/')
@app.route("/<path:url>",methods = ['POST','GET'])
def returnPage(url=""):
    if url[:7] == "record/":
        url = RECORD_PATH + url[7:]
    if os.path.isfile(url):
          return open(url, "rb" if url[-4:].lower()==".png" else "r").read()
    return "You attempted to access the url '{location}'".format(location=url)

# run the Flask app (standard Flask code)
if __name__ == '__main__':
	app.run(host="0.0.0.0",port=12345)
