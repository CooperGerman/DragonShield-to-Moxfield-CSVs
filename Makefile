# ██████╗ ██████╗  █████╗  ██████╗  ██████╗ ███╗   ██╗███████╗██╗  ██╗██╗███████╗██╗     ██████╗
# ██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔═══██╗████╗  ██║██╔════╝██║  ██║██║██╔════╝██║     ██╔══██╗
# ██║  ██║██████╔╝███████║██║  ███╗██║   ██║██╔██╗ ██║███████╗███████║██║█████╗  ██║     ██║  ██║
# ██║  ██║██╔══██╗██╔══██║██║   ██║██║   ██║██║╚██╗██║╚════██║██╔══██║██║██╔══╝  ██║     ██║  ██║
# ██████╔╝██║  ██║██║  ██║╚██████╔╝╚██████╔╝██║ ╚████║███████║██║  ██║██║███████╗███████╗██████╔╝
# ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝

# ██╗   ██╗████████╗██╗██╗     ██╗████████╗██╗███████╗███████╗
# ██║   ██║╚══██╔══╝██║██║     ██║╚══██╔══╝██║██╔════╝██╔════╝
# ██║   ██║   ██║   ██║██║     ██║   ██║   ██║█████╗  ███████╗
# ██║   ██║   ██║   ██║██║     ██║   ██║   ██║██╔══╝  ╚════██║
# ╚██████╔╝   ██║   ██║███████╗██║   ██║   ██║███████╗███████║
#  ╚═════╝    ╚═╝   ╚═╝╚══════╝╚═╝   ╚═╝   ╚═╝╚══════╝╚══════╝

# This Makefile automate, exporteing the collection from DragonShield to Archidekt
.PHONY: all export_ds convert import

default: all

# create a function that uses a python oneliner to access a json field
fetch = python -c 'import json; print(json.load(open("$(1)"))["$(2)"])'

ATTEMPTS=3

DRAGON_USER = $(shell $(call fetch,./config/config.json,dragonshield_username))
DRAGON_PASSWD = $(shell $(call fetch,./config/config.json,dragonshield_password))

ARCH_PASSWD = $(shell $(call fetch,./config/config.json,archidekt_password))
ARCH_USER = $(shell $(call fetch,./config/config.json,archidekt_username))

DLFOLDER = $(shell $(call fetch,./config/config.json,download_folder))

all: clean export_ds convert import

venv:
	echo "Setting up environment" ; \
	mkdir -p .venv ; \
	python3 -m venv .venv ; \
	echo"Installing python dependencies" ; \
	pip install -r requirements.txt --break-system-packages; \
	pip install --upgrade pip --break-system-packages; \
	echo "Done initializing virtual environment"

get_requirements:
	.venv/bin/python --force --savepath requirements.txt ./tools ; \
	deactivate

install: venv

export_ds:
	@echo "Exporting DragonShield collection to CSVs"
	.venv/bin/python tools/dragonshield_scrapper.py \
		-u=$(DRAGON_USER) \
		-p=$(DRAGON_PASSWD) \
		-a=$(ATTEMPTS)

convert: input
input:
	mkdir -p input
	cp $(DLFOLDER)/all-folder*.csv input/
	@echo "Converting CSVs to Moxfield format"
	$(MAKE) DSConvert

DSConvert:
	.venv/bin/python tools/DSConvert.py \
		./input

import:
	@echo "Importing CSVs to Archidekt"
	.venv/bin/python tools/archidekt_uploader.py \
		./results/archidekt/ \
		-u=$(ARCH_USER) \
		-p=$(ARCH_PASSWD) \
		-a=$(ATTEMPTS)

clean:
	rm -rf $(DLFOLDER)/all-folder*.csv
	rm -rf input
	rm -rf results
	rm -rf __pycache__
