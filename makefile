VENV_NAME = .venv
PACKAGE_NAME = microqa
PYTHON = ${VENV_NAME}/bin/python

.PHONY: all clean

all: clean install run

$(VENV_NAME):
	python -m venv ${VENV_NAME}

clean:
	rm -rf ${VENV_NAME}
	@echo "cleaned venv"

install: ${VENV_NAME}
	${PYTHON} -m pip install -r requirements.txt
	@echo "installed required packages"

run: install
	${PYTHON} -m ${PACKAGE_NAME}.main