Contributing to AI-Graph
========================

We welcome contributions to AI-Graph! This guide will help you get started with contributing to the project.

🎯 **Ways to Contribute**
-------------------------

- **Bug Reports**: Report issues you encounter
- **Feature Requests**: Suggest new features or improvements
- **Code Contributions**: Submit bug fixes or new features
- **Documentation**: Improve or add documentation
- **Testing**: Add tests or improve test coverage
- **Examples**: Create examples showing how to use AI-Graph

🚀 **Getting Started**
----------------------

1. **Fork the Repository**
   Fork the AI-Graph repository on GitHub.

2. **Clone Your Fork**

   .. code-block:: bash

      git clone https://github.com/your-username/ai-graph.git
      cd ai-graph

3. **Set Up Development Environment**

   .. code-block:: bash

      # Create virtual environment
      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate

      # Install in development mode
      pip install -e ".[dev]"

4. **Create a Branch**

   .. code-block:: bash

      git checkout -b feature/your-feature-name

📋 **Development Guidelines**
-----------------------------

Code Style
~~~~~~~~~~

We use several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

Run all checks:

.. code-block:: bash

   # Format code
   black ai_graph tests
   isort ai_graph tests

   # Check for issues
   flake8 ai_graph tests
   mypy ai_graph

Testing
~~~~~~~

We maintain 100% test coverage. All contributions must include tests.

.. code-block:: bash

   # Run tests
   pytest

   # Run with coverage
   pytest --cov=ai_graph --cov-report=term-missing

   # Run specific test
   pytest tests/test_pipeline.py::test_specific_function

Writing Tests
~~~~~~~~~~~~~

1. **Test Structure**: Use the AAA pattern (Arrange, Act, Assert)
2. **Test Names**: Use descriptive names that explain what is being tested
3. **Edge Cases**: Test both happy path and edge cases
4. **Fixtures**: Use pytest fixtures for common setup

Example test:

.. code-block:: python

   import pytest
   from ai_graph.step import BaseStep

   class TestBaseStep:
       def test_process_returns_correct_result(self):
           # Arrange
           step = BaseStep()
           input_data = "test"

           # Act
           result = step.process(input_data)

           # Assert
           assert result == "test"

Documentation
~~~~~~~~~~~~~

1. **Docstrings**: All public methods must have docstrings
2. **Type Hints**: Use type hints for all function parameters and return values
3. **Examples**: Include usage examples in docstrings
4. **RST Format**: Use reStructuredText format for documentation

Example docstring:

.. code-block:: python

   def process(self, data: Any) -> Any:
       """
       Process the input data.

       Args:
           data: The input data to process

       Returns:
           The processed data

       Raises:
           ValueError: If the input data is invalid

       Example:
           >>> step = MyStep()
           >>> result = step.process("input")
           >>> print(result)
           "processed input"
       """

🔧 **Development Workflow**
---------------------------

1. **Create an Issue**
   Before starting work, create an issue describing the bug or feature.

2. **Write Tests First**
   For new features, write tests that fail initially.

3. **Implement the Feature**
   Write the minimal code to make tests pass.

4. **Run All Checks**

   .. code-block:: bash

      # Run all checks
      black ai_graph tests
      isort ai_graph tests
      flake8 ai_graph tests
      mypy ai_graph
      pytest --cov=ai_graph --cov-report=term-missing

5. **Update Documentation**
   Update relevant documentation and examples.

6. **Commit Your Changes**

   .. code-block:: bash

      git add .
      git commit -m "feat: add new feature description"

7. **Push and Create PR**

   .. code-block:: bash

      git push origin feature/your-feature-name

📝 **Commit Message Guidelines**
--------------------------------

We use conventional commits for clear commit messages:

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation changes
- **test**: Adding or updating tests
- **refactor**: Code changes that neither fix a bug nor add a feature
- **style**: Code style changes (formatting, etc.)
- **chore**: Maintenance tasks

Examples:

.. code-block:: bash

   feat: add progress tracking to ForEach step
   fix: handle None values in pipeline execution
   docs: update API documentation for BaseStep
   test: add tests for error handling in pipelines

🐛 **Bug Reports**
------------------

When reporting bugs, please include:

1. **Clear Title**: Describe the issue briefly
2. **Steps to Reproduce**: Exact steps to reproduce the issue
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: Python version, OS, AI-Graph version
6. **Code Sample**: Minimal code that reproduces the issue

Bug Report Template:

.. code-block:: markdown

   **Bug Description**
   A clear description of the bug.

   **Steps to Reproduce**
   1. Create a pipeline with...
   2. Add a step that...
   3. Run the pipeline...
   4. See error

   **Expected Behavior**
   The pipeline should...

   **Actual Behavior**
   The pipeline throws...

   **Environment**
   - Python version: 3.12
   - AI-Graph version: 0.1.0
   - OS: Ubuntu 22.04

   **Code Sample**
   ```python
   # Minimal code that reproduces the issue
   ```

💡 **Feature Requests**
-----------------------

When requesting features:

1. **Use Case**: Explain the problem you're trying to solve
2. **Proposed Solution**: Describe your proposed solution
3. **Alternatives**: Consider alternative approaches
4. **Impact**: Explain how this would benefit users

Feature Request Template:

.. code-block:: markdown

   **Feature Description**
   A clear description of the feature.

   **Use Case**
   Explain the problem this feature would solve.

   **Proposed Solution**
   Describe your proposed implementation.

   **Alternatives**
   List alternative solutions you've considered.

   **Additional Context**
   Any other context or examples.

🔍 **Code Review Process**
--------------------------

1. **Automated Checks**: All PRs run automated checks (tests, linting, etc.)
2. **Manual Review**: Maintainers review code for correctness and style
3. **Feedback**: Address any feedback from reviewers
4. **Approval**: PRs need approval from at least one maintainer
5. **Merge**: Once approved, PRs are merged into main

📚 **Documentation Contributions**
----------------------------------

Documentation contributions are highly valued:

1. **API Documentation**: Auto-generated from docstrings
2. **User Guide**: Step-by-step tutorials and explanations
3. **Examples**: Real-world usage examples
4. **README**: Project overview and quick start

To build documentation locally:

.. code-block:: bash

   cd docs
   make html
   # Open _build/html/index.html in your browser

🎉 **Recognition**
------------------

Contributors are recognized in:

1. **CHANGELOG**: All contributions are listed in release notes
2. **Contributors Section**: Listed in the README
3. **Git History**: Your commits become part of the project history

📞 **Getting Help**
-------------------

If you need help:

1. **Documentation**: Check the documentation first
2. **Issues**: Search existing issues
3. **Discussions**: Use GitHub Discussions for questions
4. **Email**: Contact maintainers directly

Thank you for contributing to AI-Graph! 🙏
