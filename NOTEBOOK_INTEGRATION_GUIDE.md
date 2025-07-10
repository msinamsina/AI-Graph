# Jupyter Notebooks in Sphinx Documentation with pytest Testing

This document provides a comprehensive guide for integrating Jupyter notebooks into Sphinx documentation and testing them with pytest.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install all dependencies
pip install nbsphinx jupyter ipykernel pytest-notebook nbval

# Or install using the project's dependency groups
pip install -e ".[dev]"
```

### 2. Test Notebooks

```bash
# Test all notebooks
make test-notebooks

# Test specific notebook
pytest --nbval example/ai_graph_example.ipynb -v
```

### 3. Build Documentation

```bash
```bash
# Execute notebooks and prepare for docs
mkdir -p docs/examples
jupyter nbconvert --to notebook --execute example/*.ipynb --output-dir docs/examples

# Create index.rst for examples directory with all notebooks automatically listed
cat > docs/examples/index.rst << 'EOL'
Example Notebooks
================

.. toctree::
    :maxdepth: 1
    :caption: Examples:

EOL

# Dynamically add all notebook files to index.rst
for notebook in docs/examples/*.ipynb; do
    basename=$(basename "$notebook" .ipynb)
    echo "    $basename" >> docs/examples/index.rst
done

# Build docs with notebook integration
cd docs
make html

# Or use the API docs command
make api-docs
```

# Build docs with notebook integration
cd docs
make html

# Or use the API docs command
make api-docs
```

### 4. Serve Documentation

```bash
cd docs
make serve
```

## 📁 Project Structure

```
AI-Graph/
├── docs/
│   ├── conf.py                    # Sphinx config with nbsphinx
│   ├── docs-requirements.txt      # Updated with notebook deps
│   ├── Makefile                   # Updated with notebook commands
│   └── README.md                  # Updated with notebook info
├── example/
│   └── ai_graph_example.ipynb     # Original notebook
├── tests/
│   ├── test_notebooks.py          # Custom notebook tests
│   └── test_notebooks_nbval.py    # nbval-based tests
├── pyproject.toml                 # Updated with notebook deps
├── pytest.ini                     # Updated with nbval config
└── pytest-notebook.ini            # Notebook-only testing config
```

## 🔧 Configuration Files

### 1. Sphinx Configuration (`docs/conf.py`)

```python
extensions = [
    # ... existing extensions
    "nbsphinx",
]

# Notebook execution settings
nbsphinx_execute = "always"
nbsphinx_timeout = 60
nbsphinx_allow_errors = True
nbsphinx_kernel_name = "python3"
nbsphinx_codecell_lexer = "ipython3"
nbsphinx_prompt_width = "0"

# Exclude notebook checkpoints
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "README.md", "**.ipynb_checkpoints"]
```

### 2. Dependencies (`docs/docs-requirements.txt`)

```txt
sphinx>=4.0.0
sphinx-rtd-theme>=1.0.0
sphinx-autodoc-typehints>=1.17.0
myst-parser>=0.18.0
nbsphinx>=0.8.0
jupyter>=1.0.0
ipykernel>=6.0.0
```

### 3. Project Dependencies (`pyproject.toml`)

```toml
[dependency-groups]
test = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-notebook>=0.8.0",
    "nbval>=0.10.0",
]
docs = [
    "sphinx>=4.0.0",
    "sphinx-rtd-theme>=1.0.0",
    "sphinx-autodoc-typehints>=1.17.0",
    "myst-parser>=0.18.0",
    "nbsphinx>=0.8.0",
    "jupyter>=1.0.0",
    "ipykernel>=6.0.0",
]
```

### 4. pytest Configuration (`pytest.ini`)

```ini
[pytest]
pythonpath = .
testpaths = tests
addopts = -v --cov=ai_graph --cov-report=term-missing --cov-fail-under=90 --cov-report=xml:coverage.xml --nbval-lax

# Configure notebook testing
nbval_ignore_cells = ["# IGNORE", "# SKIP"]
nbval_timeout = 600
```

### 5. Notebook-only Testing (`pytest-notebook.ini`)

```ini
[pytest]
pythonpath = .
testpaths = tests
addopts = -v --nbval-lax

# Configure notebook testing
nbval_ignore_cells = ["# IGNORE", "# SKIP"]
nbval_timeout = 600
```

## 📖 Usage Examples

### Adding a New Notebook

1. **Create** your notebook in `example/` or appropriate location
2. **Copy** it to `docs/notebooks/` for documentation
3. **Update** `docs/notebooks/index.rst`:
   ```rst
   .. toctree::
      :maxdepth: 2
      :caption: Examples:

      ai_graph_example
      your_new_notebook
   ```
4. **Test** the notebook: `make test-notebooks`
5. **Build** documentation: `make html`

### Testing Strategies

#### Option 1: Direct nbval Testing
```bash
# Test single notebook
pytest --nbval example/ai_graph_example.ipynb -v

# Test multiple notebooks
pytest --nbval example/ docs/notebooks/ -v
```

#### Option 2: Custom Test Functions
```python
# tests/test_notebooks.py
def test_ai_graph_example_notebook():
    """Test that the AI-Graph example notebook executes without errors."""
    # Custom test logic using nbformat and ExecutePreprocessor
```

#### Option 3: Make Commands
```bash
# Test all notebooks
make test-notebooks

# Test only docs notebooks
make test-docs-nb
```

## 🎯 Best Practices

### 1. Notebook Organization
- Keep original notebooks in `example/` or similar
- Copy to `docs/notebooks/` for documentation
- Use clear, descriptive filenames

### 2. Testing Strategy
- Use `nbval` for quick validation
- Create custom tests for complex scenarios
- Test both execution and output validation

### 3. Documentation
- Add proper titles to notebooks (first markdown cell)
- Include explanatory text between code cells
- Keep notebooks focused and concise

### 4. CI/CD Integration
- Run notebook tests in CI pipeline
- Use timeout settings to prevent hanging
- Consider using `nbval-lax` for more flexible testing

## 🚨 Common Issues and Solutions

### Issue 1: Notebook Not Appearing in Docs
**Solution**: Check that the notebook is listed in `notebooks/index.rst`

### Issue 2: Execution Timeout
**Solution**: Increase timeout in `conf.py`:
```python
nbsphinx_timeout = 120  # Increase from 60
```

### Issue 3: Coverage Failures with Notebooks
**Solution**: Use separate pytest configurations or exclude notebooks from coverage:
```bash
pytest --nbval -c pytest-notebook.ini
```

### Issue 4: Build Warnings
**Solution**: Most nbsphinx warnings are non-critical. For cleaner output:
```python
nbsphinx_allow_errors = True
```

## 🔄 Workflow Summary

1. **Develop** notebook in `example/`
2. **Test** with `pytest --nbval`
3. **Copy** to `docs/notebooks/`
4. **Update** `index.rst`
5. **Test** documentation: `make test-notebooks`
6. **Build** docs: `make html`
7. **Serve** locally: `make serve`
8. **Commit** all changes

This setup provides a robust system for integrating Jupyter notebooks into your Sphinx documentation while maintaining quality through automated testing.
