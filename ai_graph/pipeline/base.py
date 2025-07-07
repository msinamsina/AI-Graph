"""
The base module for the AI Graph pipeline.

This module provides the core infrastructure for creating processing pipelines
for phase detection in eye surgeries.
"""

from typing import Any, Dict, List, Optional

from ..step.base import BasePipelineStep

# set __all__ to control what gets imported with 'from module import *'
__all__ = ["Pipeline"]


class Pipeline:
    """Class that manages the pipeline of processing steps."""

    def __init__(self, name: Optional[str], first_step: Optional[BasePipelineStep] = None):
        """
        Initialize the pipeline.

        Args:
            first_step (BasePipelineStep, optional): The first step of the pipeline.
        """
        self.name = name or self.__class__.__name__
        self.first_step = first_step
        self.steps: List[BasePipelineStep] = []
        if first_step:
            self.steps.append(first_step)

    def add_step(self, step: BasePipelineStep) -> "Pipeline":
        """
        Add a step to the pipeline.

        Args:
            step: The step to add.

        Returns:
            The pipeline instance for chaining.
        """
        if not self.first_step:
            self.first_step = step
        else:
            last_step = self.steps[-1]
            last_step.set_next(step)

        self.steps.append(step)
        return self

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the input through the entire pipeline.

        Args:
            data: Input data to be processed.

        Returns:
            The fully processed data.

        Raises:
            ValueError: If the pipeline has no steps.
        """
        if not self.first_step:
            raise ValueError("Pipeline has no steps")

        return self.first_step.process(data)
