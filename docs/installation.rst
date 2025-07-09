Installation
============

System Requirements
-------------------

AI-Graph requires Python 3.9 or higher. It has been tested on:

- Python 3.9, 3.10, 3.11, 3.12
- Windows, macOS, and Linux

Install from PyPI
-----------------

The easiest way to install AI-Graph is using pip:


.. code-block:: bash

   pip install ai-graph

If you are using `uv`, you can install it with:

.. code-block:: bash

   uv pip install ai-graph

Install from Source
-------------------

To install the latest development version from GitHub:

.. code-block:: bash

   git clone https://github.com/msinamsina/ai-graph.git
   cd ai-graph
   pip install -e .

Development Installation
------------------------

For development, install with development dependencies:

we use uv as package manager.

.. code-block:: bash

   uv sync --group dev


This will install additional tools for:

- **Testing**: pytest, pytest-cov
- **Code formatting**: black, isort
- **Linting**: flake8, mypy
- **Documentation**: sphinx, sphinx-rtd-theme, sphinx-autodoc-typehints, myst-parser
- **Development**: commitizen, twine, pre-commit, plus test, docs, and lint groups


Verification
------------

To verify your installation:

.. code-block:: python

   import ai_graph
   print(ai_graph.__version__)

Run the test suite to ensure everything is working:

.. code-block:: bash

   pytest

Docker Installation
-------------------

You can also run AI-Graph in a Docker container:

.. code-block:: bash

   docker run -it python:3.12
   pip install ai-graph

Troubleshooting
---------------

Common installation issues and solutions:

Permission Errors
~~~~~~~~~~~~~~~~~

If you encounter permission errors, try installing with the ``--user`` flag:

.. code-block:: bash

   pip install --user ai-graph

Virtual Environment
~~~~~~~~~~~~~~~~~~~

It's recommended to use a virtual environment or uv to avoid conflicts with system packages. Here's how to set one up:

.. code-block:: bash

   python -m venv ai-graph-env
   source ai-graph-env/bin/activate  # On Windows: ai-graph-env\Scripts\activate
   pip install ai-graph

.. note::

   If you are using uv, you can create a virtual environment with:

   .. code-block:: bash

      uv venv ai-graph-env
      source ai-graph-env/bin/activate
      uv pip install ai-graph


Dependency Conflicts
~~~~~~~~~~~~~~~~~~~~

If you have dependency conflicts, try creating a fresh virtual environment or use conda:

.. code-block:: bash

   conda create -n ai-graph python=3.12
   conda activate ai-graph
   pip install ai-graph
