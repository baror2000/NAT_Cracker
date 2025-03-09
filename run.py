from flask import Flask, request, jsonify
from wifi_utils import WiFiCracker

app = Flask(__name__)
wifi_cracker = WiFiCracker()

@app.route("/interfaces", methods=["GET"])
def interfaces():
    return jsonify(wifi_cracker.get_interfaces())

@app.route("/set_adapter", methods=["POST"])
def set_adapter():
    data = request.json
    return jsonify(wifi_cracker.set_adapter(data.get("adapter")))

@app.route("/scan", methods=["GET"])
def scan():
    return jsonify(wifi_cracker.scan_networks())

@app.route("/set_target", methods=["POST"])
def set_target():
    data = request.json
    return jsonify(wifi_cracker.set_target(data.get("bssid"), data.get("channel"), data.get("network_name")))

@app.route("/crack", methods=["GET"])
def crack():
    return jsonify(wifi_cracker.crack_password())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
