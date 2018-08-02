from os import environ

import json

from flask import Flask, request, make_response

from sam.requesthandlers import RequestHandler

app = Flask(__name__)


@app.route("/")
def hello():
    return "All is well and good with SAM!\n"


# @app.route("/test_weather")
# def test_weather():
#     with open('sample_weather_response.json') as json_data:
#         sample_weather_response = json.load(json_data)
#     request_handler = RequestHandler(sample_weather_response)
#     json_res = request_handler.handle_request()
#     res = make_response(json_res)
#     res.headers['Content-Type'] = 'application/json'
#     return res


@app.route('/run_sample/<sample>')
def run_sample(sample):
    try:
        json_path = 'sample_dialogflow_requests/{}.json'.format(sample)
        with open(json_path) as json_data:
            sample_dialogflow_request = json.load(json_data)
        request_handler = RequestHandler(sample_dialogflow_request)
        json_res = request_handler.handle_request()
        res = make_response(json_res)
        res.headers['Content-Type'] = 'application/json'
        return res
    except Exception as e:
        return make_response(str(e))


@app.route("/dialogflow_webhook", methods=['POST'])
def webhook():
    """
    Handle requests from dialogflow
    """
    req = request.get_json(silent=True, force=True)
    request_handler = RequestHandler(req)
    res = request_handler.handle_request()
    res = make_response(res)
    res.headers['Content-Type'] = 'application/json'
    return res


if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
