import flask
from flask import jsonify
from flask import request
from services.unbias import suggest
from services.suggestions import get_all_news
from services.classifier import get_stance
from services.classifier import is_political
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/suggestions', methods=['GET'])
def suggestions():
    return jsonify(suggest(request.args.get('headline')))

@app.route('/is_political', methods=['GET'])
def is_news_political():
	response = {
		'political' : is_political(request.args.get('headline'))
	}
	return jsonify(response)

@app.route('/political_stance', methods=['GET'])
def political_stance():
	response = {
		'stance' : get_stance(request.args.get('headline'))
	}
	return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0')