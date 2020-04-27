#!/bin/bash

export PATH=/bin:/usr/bin:/usr/local/bin:/sbin:/usr/sbin:/usr/local/sbin

echo
echo ' Install eco_logic as systemd service'
echo

SUDO=
if [ "$UID" != "0" ]; then
	if [ -e /usr/bin/sudo -o -e /bin/sudo ]; then
		SUDO=sudo
	else
		echo '*** This quick installer script requires root privileges.'
		exit 0
	fi
fi

echo
echo '*** Enabling and starting service...'

if [ -e /usr/bin/systemctl -o -e /usr/sbin/systemctl -o -e /sbin/systemctl -o -e /bin/systemctl ]; then
	$SUDO systemctl stop eco-logic
	$SUDO systemctl disable eco-logic
	$SUDO ln -fs $PWD/eco-logic.service /etc/systemd/system/eco-logic.service
	$SUDO systemctl daemon-reload
	$SUDO systemctl enable eco-logic
	$SUDO systemctl start eco-logic
	if [ "$?" != "0" ]; then
		echo
		echo '*** Package installed but cannot start service!'
		echo
		exit 1
	fi
else
	echo
	echo '*** systemctl don`t exist!'
	echo
	exit 1
fi

echo
echo '*** Done.'
echo '*** Reboot your system'

sleep 1
