#!/bin/sh

FIRMWARE_CONFIG="/boot/firmware/config.txt"
CMDLINE="/boot/firmware/cmdline.txt"
MODULES="/etc/modules"
HOMEDIR=$(eval echo ~$USER)
BASHRC="$HOMEDIR/.bashrc"

# Add necessary contents to bashrc
cat >>$BASHRC << EOL

export PATH="$HOMEDIR/.local/bin:\$PATH"
export PYTHON_KEYRING_BACKEND=keyring.backends.fail.Keyring
EOL

# Install poetry
curl -sSL https://install.python-poetry.org | python3 -

# Modify configuration files
cat >>$FIRMWARE_CONFIG << EOL
[all]
dtoverlay=dwc2 
EOL

sed -i -e 's/otg_mode=1/#otg_mode=1/g' $FIRMWARE_CONFIG

sed -i 's/$/ modules-load=dwc2,g_midi/' $CMDLINE

cat >>$MODULES << EOL 
dwc2
g_midi
EOL

source $BASHRC

poetry config virtualenvs.in-project true

cd SynthStudio
poetry update

echo "Reboot to use the device!"
