#!/bin/bash

export FIRMWARE_CONFIG="/boot/firmware/config.txt"
export CMDLINE="/boot/firmware/cmdline.txt"
export MODULES="/etc/modules"
export HOMEDIR=$(eval echo ~$SUDO_USER)
export BASHRC="$HOMEDIR/.bashrc"
export FLUIDSYNTH_SERVICE="/etc/systemd/system/fluidsynth.service"
export SYNTH_STUDIO_DIR="$PWD/SynthStudio/SynthStudio"

# Set up SSH key
read -p "Enter the email for your SSH key: " email
mkdir -p $HOMEDIR/.ssh
ssh-keygen -t ed25519 -C "$email" -f $HOMEDIR/.ssh/id_rsa -N "" -q
ssh-keyscan github.com >> $HOMEDIR/.ssh/known_hosts
echo "Add this pubkey to your GitHub account, and then press enter to continue setup."
cat $HOMEDIR/.ssh/id_rsa.pub
read temp
echo "Done!"

# Perform git clone as user
su $SUDO_USER <<'EOF'
git clone git@github.com:accrawford1/SynthStudio.git
EOF

# Add necessary contents to bashrc
echo "Modifying $BASHRC"
cat >>$BASHRC << EOL

export PATH="$HOMEDIR/.local/bin:\$PATH"
export PYTHON_KEYRING_BACKEND=keyring.backends.fail.Keyring
EOL

# Install poetry as current user, not sudo
echo "Installing poetry as $SUDO_USER"
su $SUDO_USER <<'EOF'
curl -sSL https://install.python-poetry.org | python3 -
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

su $SUDO_USER <<'EOF'
echo "Sourcing $BASHRC"
source $BASHRC

echo "Configuring poetry environment for SynthStudio"

$HOMEDIR/.local/bin/poetry config virtualenvs.in-project true

cd $SYNTH_STUDIO_DIR
$HOMEDIR/.local/bin/poetry update
EOF

echo "Updating packages before installing new ones"
apt update -qq
apt upgrade -qq

apt install --reinstall alsa-utils alsa-tools
apt install fluidsynth

cat >$FLUIDSYNTH_SERVICE << EOL
[Unit]
Description=Fluidsynth daemon
Documentation=man:fluidsynth
After=network.target

[Service]
ExecStart=/usr/bin/fluidsynth
Type=simple

[Install]
WantedBy=multi-user.target
Alias=fluidsynth.service
EOL
chmod 664 $FLUIDSYNTH_SERVICE
systemctl daemon-reload
systemctl enable --now fluidsynth

echo "Reboot to use the device!"