"""
AI-Graph Step Module.

This module provides the core step classes and utilities for building
processing pipelines using the Chain of Responsibility pattern.

The step module contains:
    - BasePipelineStep: Abstract base class for all pipeline steps
    - Built-in utility steps like AddKeyStep and DelKeyStep
    - ForEach step for iterative processing
    - Video processing steps for computer vision tasks

Example:
    >>> from ai_graph.step import BasePipelineStep
    >>> from ai_graph.pipeline import Pipeline
    >>>
    >>> class MyStep(BasePipelineStep):
    ...     def _process_step(self, data):
    ...         data['processed'] = True
    ...         return data
    >>>
    >>> pipeline = Pipeline("MyPipeline")
    >>> pipeline.add_step(MyStep())
    >>> result = pipeline.process({'input': 'data'})
"""
