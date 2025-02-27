#!/bin/bash

# Function to check if a package is installed
dependency_check() {
    dpkg -s "$1" &> /dev/null
    return $?
}

# Required packages
REQUIRED_PKGS=("aircrack-ng" "iw" "wireless-tools")
MISSING_PKGS=()

# Check each package
for pkg in "${REQUIRED_PKGS[@]}"; do
    if ! dependency_check "$pkg"; then
        MISSING_PKGS+=("$pkg")
    fi
done

# Install missing packages
if [ ${#MISSING_PKGS[@]} -gt 0 ]; then
    echo "Installing missing dependencies: ${MISSING_PKGS[*]}"
    sudo apt update
    sudo apt install -y "${MISSING_PKGS[@]}"
else
    echo "All required dependencies are already installed."
fi

# Enable monitor mode
INTERFACE=$(iw dev | awk '$1=="Interface"{print $2}')
echo "Enabling monitor mode on $INTERFACE"
sudo ip link set $INTERFACE down
sudo iw dev $INTERFACE set type monitor
sudo ip link set $INTERFACE up

echo "Setup completed successfully!"
