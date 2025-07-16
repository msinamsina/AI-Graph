.. AI-Graph documentation master file, created by
   sphinx-quickstart on Sat Jul  5 18:52:23 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

AI-Graph Documentation
=======================

.. image:: https://img.shields.io/badge/python-3.9%2B-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python Version

.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0
   :alt: License: GPL v3

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: black

Welcome to AI-Graph, a powerful and flexible framework for building AI processing pipelines using the Chain of Responsibility pattern.

🚀 **Features**
---------------

- **🔗 Pipeline Architecture**: Build complex processing pipelines using chained steps
- **🔄 ForEach Processing**: Iterate over collections or run fixed iterations with sub-pipelines
- **🏗️ Modular Design**: Easily extensible with custom pipeline steps
- **📊 Progress Tracking**: Built-in progress bars with tqdm integration
- **🧪 100% Test Coverage**: Comprehensive test suite with pytest
- **🎯 Type Safe**: Full type hints support with mypy
- **📦 Modern Python**: Built with modern Python packaging standards

📚 **Quick Start**
------------------

Installation
~~~~~~~~~~~~

.. code-block:: bash

   pip install ai-graph

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   from ai_graph.pipeline import Pipeline
   from ai_graph.step import BaseStep

   # Create a custom step
   class MyStep(BaseStep):
       def process(self, data: dict[str, any]) -> dict[str, any]:
            """
            Process data in this step.

            Parameters:
            -----------

            data (dict): Input data for this step

            key: "input" is an integer that will be processed

            Returns
            -------

            dict: Processed data
            """
            # Example processing logic
            return {"result": data["input"] * 2}
   # Build and run pipeline
   pipeline = Pipeline()
   pipeline.add_step(MyStep())
   result = pipeline.run(input_data={"input": 5})
   print(result)  # Output: {"result": 10, "input": 5}

🏗️ **Architecture Overview**
-----------------------------

AI-Graph is built around three core concepts:

1. **Steps**: Individual processing units that transform data
2. **Pipelines**: Chains of steps that process data sequentially

📖 **Documentation Contents**
-----------------------------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installation
   quick_start.ipynb
   concepts.ipynb

.. toctree::
   :maxdepth: 2
   :caption: User Guide



.. toctree::
   :maxdepth: 6
   :caption: API Reference

   api/ai_graph

.. toctree::
   :maxdepth: 2
   :caption: Examples

   notebooks/index

.. toctree::
   :maxdepth: 2
   :caption: Development

   contributing


🤝 **Contributing**
-------------------

We welcome contributions! Please see our :doc:`contributing` guide for details.

📄 **License**
--------------

This project is licensed under the GPL-3.0 License - see the `LICENSE <https://github.com/msinamsina/ai-graph/blob/main/LICENSE>`_ file for details.

🙋 **Support**
--------------

- 📖 **Documentation**: You're reading it!
- 🐛 **Issues**: `GitHub Issues <https://github.com/msinamsina/ai-graph/issues>`_
- 💬 **Discussions**: `GitHub Discussions <https://github.com/msinamsina/ai-graph/discussions>`_
- 📧 **Email**: msinamsina@gmail.com

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
