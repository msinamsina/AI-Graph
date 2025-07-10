# Makefile for AI-Graph Documentation
#
# This Makefile provides convenient commands for building documentation
# with automatic API reference generation from docstrings.

# You can set these variables from the command line.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html           to make standalone HTML files"
	@echo "  api-docs       to regenerate API documentation and build HTML"
	@echo "  regenerate-api to regenerate API documentation only"
	@echo "  serve          to serve the documentation locally"
	@echo "  clean          to remove build artifacts"
	@echo "  test-notebooks to test all notebooks in the project"


clean:
	rm -rf $(BUILDDIR)/*
	rm -rf api/

html:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

api-docs:
	@echo "Regenerating API documentation and building HTML..."
	python3 generate_docs.py
	@echo "Documentation built successfully!"

regenerate-api:
	@echo "Regenerating API documentation..."
	python3 -m sphinx.ext.apidoc -o api ../ai_graph --force --separate  --templatedir ./_templates/apidoc -d 6 -M  --remove-old -T
	@echo "Fixing module paths..."
	python3 -c "import pathlib; import re; [pathlib.Path(f).write_text(re.sub(r'.. automodule:: (step|pipeline)', r'.. automodule:: ai_graph.\1', pathlib.Path(f).read_text())) for f in pathlib.Path('api').glob('*.rst')]"
	@echo "API documentation regenerated!"

serve:
	@echo "Starting documentation server..."
	sphinx-autobuild -b html "$(SOURCEDIR)" "$(BUILDDIR)" --open-browser --port 8000 --watch "$(SOURCEDIR)" --ignore "api/*" --ignore "_build/*" --ignore "venv/*" --ignore ".git/*"

test-notebooks:
	@echo "Testing all notebooks in the project..."
	cd .. && python -m pytest --nbval -c pytest-notebook.ini example/ docs/notebooks/ -v

.PHONY: help clean html api-docs regenerate-api serve test-notebooks

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
