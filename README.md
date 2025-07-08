# AI-Graph

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://img.shields.io/badge/tests-pytest-green.svg)](https://pytest.org/)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/pytest-dev/pytest-cov)
[![Development Status](https://img.shields.io/badge/status-alpha-orange.svg)](https://pypi.org/classifiers/)

> A powerful and flexible AI Graph framework for building processing pipelines using the Chain of Responsibility pattern.

## 🚀 Features

- **🔗 Pipeline Architecture**: Build complex processing pipelines using chained steps
- **🔄 ForEach Processing**: Iterate over collections or run fixed iterations with sub-pipelines
- **🏗️ Modular Design**: Easily extensible with custom pipeline steps
- **📊 Progress Tracking**: Built-in progress bars with tqdm integration
- **🧪 100% Test Coverage**: Comprehensive test suite with pytest
- **🎯 Type Safe**: Full type hints support with mypy
- **📦 Modern Python**: Built with modern Python packaging standards

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Concepts](#core-concepts)
  - [Pipeline Steps](#pipeline-steps)
  - [Pipelines](#pipelines)
  - [ForEach Processing](#foreach-processing)
- [Examples](#examples)
- [API Reference](#api-reference)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## 💾 Installation

### Using pip

```bash
pip install ai-graph
```

### Using uv (recommended)

```bash
uv add ai-graph
```

### Development Installation

```bash
git clone https://github.com/ai-graph/ai-graph.git
cd ai-graph
uv sync --group dev
```

## ⚡ Quick Start

Here's a simple example to get you started:

```python
from ai_graph.pipeline.base import Pipeline
from ai_graph.step.base import AddKeyStep, DelKeyStep
from ai_graph.step.foreach import ForEachStep

# Create a simple pipeline
pipeline = Pipeline("DataProcessor")

# Add processing steps
pipeline.add_step(AddKeyStep("status", "processing"))
pipeline.add_step(AddKeyStep("timestamp", "2024-01-01"))

# Process data
data = {"input": "some data"}
result = pipeline.process(data)

print(result)
# Output: {'input': 'some data', 'status': 'processing', 'timestamp': '2024-01-01'}
```

## 🧩 Core Concepts

### Pipeline Steps

Pipeline steps are the building blocks of your processing pipeline. Each step implements the `BasePipelineStep` interface:

```python
from ai_graph.step.base import BasePipelineStep

class CustomStep(BasePipelineStep):
    def _process_step(self, data):
        # Your processing logic here
        data["custom_field"] = "processed"
        return data

# Use in pipeline
pipeline = Pipeline("CustomPipeline")
pipeline.add_step(CustomStep("MyCustomStep"))
```

### Built-in Steps

- **`AddKeyStep`**: Adds a key-value pair to the data
- **`DelKeyStep`**: Removes a key from the data
- **`ForEachStep`**: Processes collections or runs iterations

### Pipelines

Pipelines manage the execution flow of your processing steps:

```python
from ai_graph.pipeline.base import Pipeline

# Create pipeline
pipeline = Pipeline("MyPipeline")

# Add steps (method chaining supported)
pipeline.add_step(step1).add_step(step2).add_step(step3)

# Process data
result = pipeline.process(input_data)
```

### ForEach Processing

Process collections or run fixed iterations with sub-pipelines:

```python
from ai_graph.step.foreach import ForEachStep

# Process a list of items
foreach_step = ForEachStep(
    items_key="items",
    results_key="processed_items"
)

# Add sub-processing steps
foreach_step.add_sub_step(AddKeyStep("processed", True))
foreach_step.add_sub_step(AddKeyStep("batch_id", "batch_001"))

# Use in pipeline
pipeline = Pipeline("BatchProcessor")
pipeline.add_step(foreach_step)

data = {"items": [{"id": 1}, {"id": 2}, {"id": 3}]}
result = pipeline.process(data)
```

## 📚 Examples

### Example 1: Data Validation Pipeline

```python
from ai_graph.pipeline.base import Pipeline
from ai_graph.step.base import AddKeyStep

class ValidateDataStep(BasePipelineStep):
    def _process_step(self, data):
        if "required_field" not in data:
            data["validation_error"] = "Missing required field"
        else:
            data["validation_status"] = "valid"
        return data

# Create validation pipeline
pipeline = Pipeline("DataValidator")
pipeline.add_step(ValidateDataStep("Validator"))
pipeline.add_step(AddKeyStep("validated_at", "2024-01-01"))

# Process data
data = {"required_field": "value"}
result = pipeline.process(data)
```

### Example 2: Batch Processing with ForEach

```python
from ai_graph.step.foreach import ForEachStep

class ProcessItemStep(BasePipelineStep):
    def _process_step(self, data):
        # Access current item and iteration index
        current_item = data["_current_item"]
        iteration_index = data["_iteration_index"]

        # Process the item
        data["processed_value"] = current_item * 2
        data["position"] = iteration_index

        return data

# Create batch processing pipeline
batch_processor = ForEachStep(
    items_key="numbers",
    results_key="processed_numbers"
)
batch_processor.add_sub_step(ProcessItemStep("ItemProcessor"))

pipeline = Pipeline("BatchProcessor")
pipeline.add_step(batch_processor)

# Process batch
data = {"numbers": [1, 2, 3, 4, 5]}
result = pipeline.process(data)
# result["processed_numbers"] will contain processed items
```

### Example 3: Fixed Iterations

```python
# Run a fixed number of iterations
iteration_step = ForEachStep(
    iterations=5,
    results_key="iteration_results"
)

class IterationStep(BasePipelineStep):
    def _process_step(self, data):
        iteration = data["_iteration_index"]
        data["step"] = f"Step {iteration + 1}"
        return data

iteration_step.add_sub_step(IterationStep("Iterator"))

pipeline = Pipeline("IterationPipeline")
pipeline.add_step(iteration_step)

result = pipeline.process({"start": True})
```

## 📖 API Reference

### BasePipelineStep

```python
class BasePipelineStep:
    def __init__(self, name: str = None)
    def set_next(self, step: 'BasePipelineStep') -> None
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]
    def _process_step(self, data: Dict[str, Any]) -> Dict[str, Any]  # Override this
```

### Pipeline

```python
class Pipeline:
    def __init__(self, name: str, first_step: Optional[PipelineStep] = None)
    def add_step(self, step: PipelineStep) -> "Pipeline"
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]
```

### ForEachStep

```python
class ForEachStep(BasePipelineStep):
    def __init__(
        self,
        items_key: Optional[str] = None,
        iterations: Optional[int] = None,
        results_key: str = "foreach_results",
        name: str = None
    )
    def add_sub_step(self, step: BasePipelineStep) -> "ForEachStep"
```

## 🛠️ Development

### Prerequisites

- Python 3.8+
- uv (recommended) or pip

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/ai-graph/ai-graph.git
cd ai-graph

# Install dependencies
uv sync --group dev

# Install pre-commit hooks (optional)
uv run pre-commit install
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Run specific test file
uv run pytest tests/step/test_base.py
```

### Code Quality

```bash
# Format code
uv run black .
uv run isort .

# Lint code
uv run flake8 .

# Type checking
uv run mypy .
```

### Making Releases

This project uses conventional commits and automated versioning:

```bash
# Make changes and commit using conventional commits
uv run cz commit

# Bump version automatically
uv run cz bump

# Push changes and tags
git push origin main --tags
```

## 🤝 Contributing

We love contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Ensure tests pass: `uv run pytest`
5. Format code: `uv run black . && uv run isort .`
6. Commit using conventional commits: `uv run cz commit`
7. Push and create a Pull Request

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

- 📧 Email: [msinamsina@gmail.com](mailto:msinamsina@gmail.com)
- 🐛 Issues: [GitHub Issues](https://github.com/ai-graph/ai-graph/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/ai-graph/ai-graph/discussions)

## 🎉 Acknowledgments

- Built with modern Python packaging standards
- Inspired by the Chain of Responsibility design pattern
- Uses [tqdm](https://github.com/tqdm/tqdm) for progress bars
- Tested with [pytest](https://pytest.org/)

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ by [Mohammad Sina Allahkaram](https://github.com/msinamsina)

</div>
