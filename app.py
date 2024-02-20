from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'IO_END'

@app.route('/run', methods=["POST"])
def run_code():
    run = subprocess.run(request.data.decode("utf-8"), shell=True, stdout=subprocess.PIPE,  stderr=subprocess.PIPE, encoding="utf-8")
    if run.stdout:
        return run.stdout
    else:
        return run.stderr

@app.route('/eval', methods=["POST"])
def proo():
   text = request.data.decode("utf-8")
   if not text:
      return "lol"
   file = io.StringIO()
   sys.stdout = file
   sys.stderr = file
   try:
      exec(text)
   except Exception:
      return traceback.format_exc()
   sys.stdout = sys.__stdout__
   sys.stderr = sys.__stderr__
   return file.getvalue()
