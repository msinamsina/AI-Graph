"""Tests for ai_graph.pipeline.base module."""

from unittest.mock import MagicMock

import pytest

from ai_graph.pipeline.base import Pipeline
from ai_graph.step.base import BasePipelineStep


class TestPipeline:
    """
    Test class for Pipeline.

    This class contains tests for the Pipeline class,
    which manages the pipeline of processing steps in the AI Graph framework.
    """

    @pytest.fixture
    def mock_step(self):
        """Fixture that provides a mock BasePipelineStep for testing."""
        step = MagicMock(spec=BasePipelineStep)
        step.name = "MockStep"
        return step

    @pytest.fixture
    def pipeline(self):
        """Fixture that provides a basic Pipeline instance for testing."""
        return Pipeline("TestPipeline")

    @pytest.fixture
    def pipeline_with_step(self, mock_step):
        """Fixture that provides a Pipeline instance with a first step for testing."""
        return Pipeline("TestPipeline", mock_step)

    class TestDunderInit:
        """
        Test class for the __init__ method of Pipeline.

        This class contains tests for the initialization of the Pipeline class.
        """

        def test_init_without_first_step(self):
            """Test that the __init__ method initializes the pipeline correctly without a first step."""
            pipeline = Pipeline("TestPipeline")
            assert pipeline.name == "TestPipeline"
            assert pipeline.first_step is None
            assert pipeline.steps == []

        def test_init_with_first_step(self, mock_step):
            """Test that the __init__ method initializes the pipeline correctly with a first step."""
            pipeline = Pipeline("TestPipeline", mock_step)
            assert pipeline.name == "TestPipeline"
            assert pipeline.first_step == mock_step
            assert pipeline.steps == [mock_step]

        def test_init_with_none_name(self, mock_step):
            """Test that the __init__ method uses class name when name is None."""
            pipeline = Pipeline(None, mock_step)
            assert pipeline.name == "Pipeline"
            assert pipeline.first_step == mock_step
            assert pipeline.steps == [mock_step]

    class TestAddStep:
        """
        Test class for the add_step method of Pipeline.

        This class contains tests for adding steps to the pipeline.
        """

        def test_add_step_to_empty_pipeline(self, pipeline, mock_step):
            """Test that the add_step method adds a step to an empty pipeline correctly."""
            result = pipeline.add_step(mock_step)

            assert result == pipeline  # Method should return self for chaining
            assert pipeline.first_step == mock_step
            assert pipeline.steps == [mock_step]

        def test_add_step_to_pipeline_with_existing_step(self, pipeline_with_step, mock_step):
            """Test that the add_step method adds a step to a pipeline with existing steps."""
            new_step = MagicMock(spec=BasePipelineStep)
            new_step.name = "NewMockStep"

            result = pipeline_with_step.add_step(new_step)

            assert result == pipeline_with_step  # Method should return self for chaining
            assert pipeline_with_step.first_step == mock_step  # First step should remain unchanged
            assert pipeline_with_step.steps == [mock_step, new_step]
            mock_step.set_next.assert_called_once_with(new_step)

        def test_add_multiple_steps_chaining(self, pipeline):
            """Test that multiple steps can be added using method chaining."""
            step1 = MagicMock(spec=BasePipelineStep)
            step2 = MagicMock(spec=BasePipelineStep)
            step3 = MagicMock(spec=BasePipelineStep)

            result = pipeline.add_step(step1).add_step(step2).add_step(step3)

            assert result == pipeline
            assert pipeline.first_step == step1
            assert pipeline.steps == [step1, step2, step3]
            step1.set_next.assert_called_once_with(step2)
            step2.set_next.assert_called_once_with(step3)

    class TestProcess:
        """
        Test class for the process method of Pipeline.

        This class contains tests for processing data through the pipeline.
        """

        def test_process_with_empty_pipeline(self, pipeline):
            """Test that the process method raises ValueError when pipeline has no steps."""
            data = {"key": "value"}

            with pytest.raises(ValueError, match="Pipeline has no steps"):
                pipeline.process(data)

        def test_process_with_single_step(self, pipeline_with_step, mock_step):
            """Test that the process method processes data through a single step."""
            data = {"input": "data"}
            expected_output = {"output": "processed_data"}
            mock_step.process.return_value = expected_output

            result = pipeline_with_step.process(data)

            assert result == expected_output
            mock_step.process.assert_called_once_with(data)

        def test_process_with_multiple_steps(self, pipeline):
            """Test that the process method processes data through multiple steps."""
            # Create mock steps
            step1 = MagicMock(spec=BasePipelineStep)
            step2 = MagicMock(spec=BasePipelineStep)

            # Set up the pipeline
            pipeline.add_step(step1).add_step(step2)

            # Set up mock returns
            final_data = {"final": "data"}
            step1.process.return_value = final_data

            input_data = {"input": "data"}

            result = pipeline.process(input_data)

            assert result == final_data
            step1.process.assert_called_once_with(input_data)
            # Note: step2.process is not called directly since step1.process handles the chain

        @pytest.mark.parametrize(
            "data",
            [
                {},
                {"key": "value"},
                {"multiple": "keys", "in": "dict"},
                {"nested": {"dict": {"with": "values"}}},
            ],
        )
        def test_process_with_various_data_types(self, pipeline_with_step, mock_step, data):
            """Test that the process method handles various data types correctly."""
            expected_output = {**data, "processed": True}
            mock_step.process.return_value = expected_output

            result = pipeline_with_step.process(data)

            assert result == expected_output
            mock_step.process.assert_called_once_with(data)
