venvDir := ~/.venv

# Sets the default target for the makefile.
default: run

# Starts Ollama.
serve:
	ollama serve

# Setup the virtual environment and dependencies.
setup:
	@( \
		if [ -d $(venvDir) ]; then rm -Rf $(venvDir); fi; \
		mkdir $(venvDir); \
		python3 -m venv $(venvDir); \
    	source $(venvDir)/bin/activate; \
       	python3 -m pip install -r requirements.txt --upgrade; \
    )

# Starts the chat application.
run:
	@( \
    	source $(venvDir)/bin/activate; \
		streamlit run app.py; \
    )