activate:
	if [ -d "venv" ]; then \
        echo "Python 🐍 environment was activated"; \
    else \
        echo "The folder environment doesn't exist"; \
        echo "The environment folder was created and the python 🐍 environment was activated"; \
    fi
	. ./venv/bin/activate

install:
	pip3 install -r requirements.txt

run:
	@if [ -z "$(strip $(PORT))" ]; then \
		flask run; \
	else \
		flask run -p $(PORT); \
	fi