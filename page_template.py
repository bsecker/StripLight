from flask import Flask, render_template
import datetime
app = Flask(__name__)

@app.route("/")
def hello():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   templateData = {
      'title' : 'hello world!',
      'time': timeString
      }
   return render_template('main.html', **templateData)

if __name__ == "__main__":
   app.run(host='127.0.0.1', port=80, debug=True)