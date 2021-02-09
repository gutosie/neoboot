#!/bin/sh
#DESCRIPTION=This script by gutosie

opkg update
opkg install --force-reinstall mtd-utils
opkg install --force-reinstall mtd-utils-ubifs
opkg install --force-reinstall mtd-utils-jffs2
opkg install --force-reinstall kernel-module-nandsim
opkg install --force-reinstall python-subprocess
opkg install --force-reinstall python-argparse
opkg install --force-reinstall curl
opkg install --force-reinstall liblzo2-2
opkg install --force-reinstall python-imaging
opkg install --force-maintainer --force-reinstall --force-overwrite kernel-image
opkg configure update-modules
cd
