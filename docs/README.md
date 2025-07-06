# AI-Graph Documentation

This folder contains the Sphinx documentation for the AI-Graph project.

## 🚀 Quick Start

### Prerequisites

Install the documentation dependencies:

```bash
pip install -e ".[docs]"
```

Or install them manually:

```bash
pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints myst-parser
```

### Building the Documentation

To build the HTML documentation:

```bash
cd docs
make html
```

The built documentation will be available in `_build/html/index.html`.

### Live Development

For development, you can use the auto-build feature:

```bash
cd docs
sphinx-autobuild . _build/html
```

This will automatically rebuild the documentation when files change and serve it at `http://localhost:8000`.

## 📁 Structure

```
docs/
├── _build/          # Built documentation (generated)
├── _static/         # Static assets (CSS, JS, images)
│   ├── css/
│   │   └── custom.css      # Custom styling
│   ├── js/
│   │   └── custom.js       # Custom JavaScript
│   └── images/
│       └── logo.svg        # Project logo
├── _templates/      # Custom Sphinx templates
│   └── layout.html         # Base template with custom header/footer
├── api/             # API documentation
│   ├── pipeline.rst
│   ├── step.rst
│   └── foreach.rst
├── examples/        # Usage examples
│   └── basic-pipeline.rst
├── conf.py          # Sphinx configuration
├── index.rst        # Main documentation index
├── installation.rst # Installation guide
├── quick-start.rst  # Quick start guide
├── concepts.rst     # Core concepts
├── contributing.rst # Contributing guide
├── changelog.rst    # Changelog
└── roadmap.rst      # Project roadmap
```

## 🎨 Custom Theme

The documentation uses a custom theme based on the Read the Docs theme with:

- **Custom CSS**: Modern gradient styling with AI-Graph branding
- **Custom JavaScript**: Enhanced functionality including:
  - Copy buttons for code blocks
  - Back to top button
  - Reading progress indicator
  - Search highlighting
  - Dark mode toggle
  - Keyboard shortcuts
- **Custom Templates**: Enhanced layout with custom header and footer
- **Responsive Design**: Mobile-friendly responsive layout

## 🔧 Configuration

Key configuration options in `conf.py`:

- **Theme**: `sphinx_rtd_theme` with custom styling
- **Extensions**: Auto-documentation, type hints, MyST parser
- **Custom Assets**: CSS, JavaScript, and images
- **Intersphinx**: Links to Python, NumPy documentation
- **MyST Parser**: Markdown support with extensions

## 📝 Writing Documentation

### RestructuredText (.rst files)

Most documentation is written in RestructuredText format:

```rst
Title
=====

Subtitle
--------

- **Bold text**
- *Italic text*
- ``Code text``

.. code-block:: python

   # Python code example
   from ai_graph import Pipeline

.. note::
   This is a note admonition.
```

### Markdown (.md files)

You can also use Markdown thanks to the MyST parser:

```markdown
# Title

## Subtitle

- **Bold text**
- *Italic text*
- `Code text`

```python
# Python code example
from ai_graph import Pipeline
```

```{note}
This is a note admonition.
```

### API Documentation

API documentation is automatically generated from docstrings:

```python
def my_function(param: str) -> str:
    """
    Short description.

    Args:
        param: Description of parameter

    Returns:
        Description of return value

    Example:
        >>> my_function("hello")
        "hello"
    """
    return param
```

## 🚀 Deployment

### GitHub Pages

The documentation can be deployed to GitHub Pages:

1. Build the documentation: `make html`
2. Copy `_build/html/*` to your GitHub Pages repository
3. Commit and push

### Read the Docs

The documentation is configured for Read the Docs:

1. Connect your repository to Read the Docs
2. The build will automatically use the configuration in `conf.py`
3. Documentation will be available at `https://your-project.readthedocs.io`

## 🎯 Features

- **Modern Design**: Custom gradient theme with AI-Graph branding
- **Responsive**: Works on desktop, tablet, and mobile
- **Interactive**: Copy buttons, search, progress indicators
- **Accessible**: Keyboard navigation and screen reader support
- **Fast**: Optimized for performance with lazy loading
- **SEO Friendly**: Proper meta tags and structured data

## 🔍 Search

The documentation includes full-text search powered by Sphinx's built-in search functionality.

## 📊 Analytics

To add analytics, update the `html_theme_options` in `conf.py`:

```python
html_theme_options = {
    'analytics_id': 'your-analytics-id',
    'analytics_anonymize_ip': False,
}
```

## 🤝 Contributing

To contribute to the documentation:

1. Edit the relevant `.rst` or `.md` files
2. Build and test locally: `make html`
3. Check for warnings and fix them
4. Submit a pull request

## 📞 Support

For documentation-related questions:

- Check the [Sphinx documentation](https://www.sphinx-doc.org/)
- Read the [Read the Docs tutorial](https://docs.readthedocs.io/)
- Open an issue in the GitHub repository
