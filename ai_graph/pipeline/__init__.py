"""
AI-Graph Pipeline Module.

This module provides the core pipeline management functionality for AI-Graph,
allowing you to chain together multiple processing steps in a Chain of Responsibility pattern.

The pipeline module contains:
    - Pipeline: Main class for managing and executing pipeline steps
    - Utilities for pipeline construction and management

Example:
    >>> from ai_graph.pipeline import Pipeline
    >>> from ai_graph.step import AddKeyStep, DelKeyStep
    >>>
    >>> # Create a pipeline with multiple steps
    >>> pipeline = Pipeline("DataProcessor")
    >>> pipeline.add_step(AddKeyStep("status", "processing"))
    >>> pipeline.add_step(AddKeyStep("timestamp", "2025-01-01"))
    >>> pipeline.add_step(DelKeyStep("temp_data"))
    >>>
    >>> # Execute the pipeline
    >>> result = pipeline.process({"input": "data", "temp_data": "remove_me"})
    >>> # result = {"input": "data", "status": "processing", "timestamp": "2025-01-01"}
"""
