#!/bin/dash -e

# Setup dpkg
export DEBIAN_FRONTEND=noninteractive
export DEBCONF_NONINTERACTIVE_SEEN=true

# Install extra packages (this should be moved)
apt-get -q -y install `cat $1/target.pkgs | grep -v "^\ *#"`
