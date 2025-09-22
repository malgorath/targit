# Makefile for targit
# Usage:
#   make        # Creates a binary 'targit' in the current directory

PYTHON=python3
PYINSTALLER=pyinstaller
SCRIPT=targit.py
BINARY=targit

all: $(BINARY)

$(BINARY): $(SCRIPT)
	$(PYINSTALLER) --onefile --name $(BINARY) $(SCRIPT)
	@echo "Binary '$(BINARY)' created in dist/ directory."

clean:
	rm -rf dist build *.spec
	@echo "Cleaned build artifacts."

.PHONY: all clean
