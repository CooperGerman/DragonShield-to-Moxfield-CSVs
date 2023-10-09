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

DLFOLDER = $(shell $(call fetch,./config/config.json,dragonshield_download_folder))

all: clean export_ds convert import

export_ds:
	@echo "Exporting DragonShield collection to CSVs"
	python tools/dragonshield_scrapper.py \
		-u=$(DRAGON_USER) \
		-p=$(DRAGON_PASSWD) \
		-a=$(ATTEMPTS)

convert: input
input:
	mkdir -p input
	cp $(DLFOLDER)/all-folder*.csv input/
	@echo "Converting CSVs to Moxfield format"
	python tools/DSConvert.py \
		./input

import:
	@echo "Importing CSVs to Archidekt"
	python tools/archidekt_uploader.py \
		./results/archidekt/ \
		-u=$(ARCH_USER) \
		-p=$(ARCH_PASSWD) \
		-a=$(ATTEMPTS)

clean:
	rm -rf $(DLFOLDER)/all-folder*.csv
	rm -rf input
	rm -rf results
	rm -rf __pycache__
