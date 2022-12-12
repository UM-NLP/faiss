import flask
import search_engine as se
from flask import request, jsonify
import  json
from waitress import serve
initialized = False
app = flask.Flask(__name__)
app.config["DEBUG"] = True
@app.route('/', methods=['GET'])
def home():
    return "I'm alive!"

@app.route('/search_765', methods=['POST'])
def search_765():
    request_data = request.get_json()
    text = request_data['text']
    result=se.search_765(text)
    result=json.dumps({'respond': result})
    return result
if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5001)

