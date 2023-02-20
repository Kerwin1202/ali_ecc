from flask import Flask, request, Response, jsonify, render_template
import sys
from ali import sign


server = Flask(__name__)


@server.route('/alisign', methods=['GET'])
def aliSign():
    userId = request.args.get('userid')
    deviceId = request.args.get('deviceid')
    jwt = request.args.get('jwt')
    result = {}
    result["sign"] = sign(deviceId, userId, jwt)
    return jsonify(result)


if __name__ == '__main__':
    port = 19951
    if (len(sys.argv) > 1):
        port = sys.argv[1]
    server.run(host='0.0.0.0', port=port)
