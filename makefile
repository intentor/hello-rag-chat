venvDir := ~/.venv

# Sets the default target for the makefile.
default: run

# Starts Ollama.
serve:
	ollama serve

# Setup virtual environment for Python.
venv:
	if [ -d $(venvDir) ]; then rm -Rf $(venvDir); fi
	mkdir $(venvDir)
	python3 -m venv $(venvDir)

# Opens the dashboard to visualize the expenses.
run:
	@( \
    	source $(venvDir)/bin/activate; \
       	python3 -m pip install -r requirements.txt --upgrade; \
		streamlit run app.py; \
    )