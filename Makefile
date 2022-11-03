#---------------------------------
# Discord Bot
# Makefile
#
# @ start date          01 11 2022
# @ last update         01 11 2022
#---------------------------------
SHELL := /bin/bash

install:
	@echo "Installing discord-bot..."

	pip3 install -r requirements.txt
	pip3 install .

clean:
	pip3 uninstall discord-bot --yes