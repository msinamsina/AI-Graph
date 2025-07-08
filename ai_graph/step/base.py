"""Base classes for pipeline steps."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

__all__ = [
    "BasePipelineStep",
]


class BasePipelineStep(ABC):
    """Abstract base class for pipeline steps in a Chain of Responsibility pattern.

    Each pipeline step can process input data and pass it to the next step.
    """

    def __init__(self, name: Optional[str] = None):
        """
        Initialize a pipeline step.

        Args:
            name (str, optional): A descriptive name for this pipeline step.
        """
        self.name = name or self.__class__.__name__
        self._next_step: Optional["BasePipelineStep"] = None

    def set_next(self, step: "BasePipelineStep") -> "BasePipelineStep":
        """
        Set the next step in the pipeline chain.

        Args:
            step: The next step in the pipeline.

        Returns:
            The next step for chaining purposes.
        """
        self._next_step = step
        return step

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the input data and pass to the next step if available.

        Args:
            data: Input data to be processed.

        Returns:
            Processed data.
        """
        result = self._process_step(data)

        if self._next_step:
            return self._next_step.process(result)
        return result

    @abstractmethod
    def _process_step(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the current step.

        Must be implemented by concrete pipeline steps.

        Args:
            data: Input data to be processed.

        Returns:
            Processed data.
        """
        raise NotImplementedError()


class AddKeyStep(BasePipelineStep):
    """
    A simple step that adds a specified key-value pair to the input data.

    This is useful for augmenting data before passing it to the next step.
    """

    def __init__(self, key: str, value: Any, name: Optional[str] = None):
        """
        Initialize the step with the key and value to be added.

        Args:
            key (str): The key to add to the input data.
            value (Any): The value associated with the key.
            name (str, optional): Name of this pipeline step.
        """
        super().__init__(name or "AddKeyStep")
        self._key = key
        self._value = value

    def _process_step(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add the specified key-value pair to the input data."""
        data[self._key] = self._value
        return data


class DelKeyStep(BasePipelineStep):
    """
    A simple step that deletes a specified key from the input data.

    This is useful for cleaning up data before passing it to the next step.
    """

    def __init__(self, key: str, name: Optional[str] = None):
        """
        Initialize the step with the key to be deleted.

        Args:
            key (str): The key to delete from the input data.
            name (str, optional): Name of this pipeline step.
        """
        super().__init__(name or "DelKeyStep")
        self._key = key

    def _process_step(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Delete the specified key from the input data."""
        if self._key in data:
            del data[self._key]
        return data
