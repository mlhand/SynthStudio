#!/bin/sh

FIRMWARE_CONFIG="/boot/firmware/config.txt"
CMDLINE="/boot/firmware/cmdline.txt"
MODULES="/etc/modules"
HOMEDIR=$(eval echo ~$SUDO_USER)
BASHRC="$HOMEDIR/.bashrc"

# Add necessary contents to bashrc
echo "Modifying $BASHRC"
cat >>$BASHRC << EOL

export PATH="$HOMEDIR/.local/bin:\$PATH"
export PYTHON_KEYRING_BACKEND=keyring.backends.fail.Keyring
EOL

# Install poetry as current user, not sudo
echo "Installing poetry as $SUDO_USER"
su $SUDO_USER <<'EOF'
curl -sSL https://install.python-poetry.org | python3 - && echo $USER
EOF

# Modify configuration files
echo "Modifying $FIRMWARE_CONFIG"
cat >>$FIRMWARE_CONFIG << EOL
[all]
dtoverlay=dwc2 
EOL

sed -i -e 's/otg_mode=1/#otg_mode=1/g' $FIRMWARE_CONFIG

echo "Modifying $CMDLINE"
sed -i 's/$/ modules-load=dwc2,g_midi/' $CMDLINE

echo "Modifying $MODULES"
cat >>$MODULES << EOL 
dwc2
g_midi
EOL

echo "Sourcing $BASHRC"
. $BASHRC

echo "Configuring poetry environment for SynthStudio"

poetry config virtualenvs.in-project true

cd SynthStudio
poetry update

echo "Reboot to use the device!"
