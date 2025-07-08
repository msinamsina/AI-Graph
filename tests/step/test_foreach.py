"""Tests for the ForEachStep class in the AI Graph framework."""

from unittest.mock import MagicMock, patch

import pytest

from ai_graph.step.base import BasePipelineStep
from ai_graph.step.foreach import ForEachStep


class TestForEachStep:
    """
    Test class for ForEachStep.

    This class contains tests for the ForEachStep class,
    which processes each item in a collection or runs a fixed number of iterations in the AI Graph framework.
    """

    @pytest.fixture
    def mock_sub_step(self):
        """Fixture that provides a mock BasePipelineStep for sub-pipeline testing."""
        step = MagicMock(spec=BasePipelineStep)
        step.name = "MockSubStep"
        return step

    @pytest.fixture
    def foreach_step_with_items(self):
        """Fixture that provides a ForEachStep configured to iterate over items."""
        return ForEachStep(items_key="items", results_key="results")

    @pytest.fixture
    def foreach_step_with_iterations(self):
        """Fixture that provides a ForEachStep configured to run a fixed number of iterations."""
        return ForEachStep(iterations=3, results_key="results")

    class TestDunderInit:
        """
        Test class for the __init__ method of ForEachStep.

        This class contains tests for the initialization of the ForEachStep class.
        """

        def test_init_with_items_key(self):
            """Test that the __init__ method initializes the step correctly with items_key."""
            step = ForEachStep(items_key="test_items", results_key="test_results")
            assert step.name == "ForEachStep"
            assert step.items_key == "test_items"
            assert step.iterations is None
            assert step.results_key == "test_results"
            assert step.sub_pipeline.name == "ForEachStep_SubPipeline"

        def test_init_with_iterations(self):
            """Test that the __init__ method initializes the step correctly with iterations."""
            step = ForEachStep(iterations=5, results_key="test_results")
            assert step.name == "ForEachStep"
            assert step.items_key is None
            assert step.iterations == 5
            assert step.results_key == "test_results"
            assert step.sub_pipeline.name == "ForEachStep_SubPipeline"

        def test_init_with_custom_name(self):
            """Test that the __init__ method initializes the step correctly with a custom name."""
            step = ForEachStep(items_key="items", name="CustomForEach")
            assert step.name == "CustomForEach"
            assert step.sub_pipeline.name == "CustomForEach_SubPipeline"

        def test_init_with_both_items_key_and_iterations(self):
            """Test that the __init__ method works when both items_key and iterations are provided."""
            step = ForEachStep(items_key="items", iterations=3, results_key="results")
            assert step.items_key == "items"
            assert step.iterations == 3

        def test_init_without_items_key_or_iterations_raises_error(self):
            """Test that the __init__ method raises ValueError when neither items_key nor iterations is provided."""
            with pytest.raises(ValueError, match="Either items_key or iterations must be provided"):
                ForEachStep()

    class TestAddSubStep:
        """
        Test class for the add_sub_step method of ForEachStep.

        This class contains tests for adding steps to the sub-pipeline.
        """

        def test_add_sub_step(self, foreach_step_with_items, mock_sub_step):
            """Test that the add_sub_step method adds a step to the sub-pipeline correctly."""
            result = foreach_step_with_items.add_sub_step(mock_sub_step)

            assert result == foreach_step_with_items  # Method should return self for chaining
            assert mock_sub_step in foreach_step_with_items.sub_pipeline.steps

        def test_add_multiple_sub_steps_chaining(self, foreach_step_with_items):
            """Test that multiple sub-steps can be added using method chaining."""
            step1 = MagicMock(spec=BasePipelineStep)
            step2 = MagicMock(spec=BasePipelineStep)
            step3 = MagicMock(spec=BasePipelineStep)

            result = foreach_step_with_items.add_sub_step(step1).add_sub_step(step2).add_sub_step(step3)

            assert result == foreach_step_with_items
            assert step1 in foreach_step_with_items.sub_pipeline.steps
            assert step2 in foreach_step_with_items.sub_pipeline.steps
            assert step3 in foreach_step_with_items.sub_pipeline.steps

    class TestGetItems:
        """
        Test class for the _get_items method of ForEachStep.

        This class contains tests for getting items to iterate over.
        """

        def test_get_items_with_items_key(self, foreach_step_with_items):
            """Test that _get_items returns items from data when items_key is present."""
            data = {"items": [1, 2, 3, 4]}
            items = foreach_step_with_items._get_items(data)
            assert list(items) == [1, 2, 3, 4]

        def test_get_items_with_missing_items_key(self, foreach_step_with_items):
            """Test that _get_items returns empty range when items_key is not in data."""
            data = {"other_key": "value"}
            items = foreach_step_with_items._get_items(data)
            assert list(items) == []

        def test_get_items_with_iterations(self, foreach_step_with_iterations):
            """Test that _get_items returns range when using iterations."""
            data = {"some_key": "value"}
            items = foreach_step_with_iterations._get_items(data)
            assert list(items) == [0, 1, 2]

        @pytest.mark.parametrize(
            "items",
            [
                [],
                [1],
                [1, 2, 3],
                ["a", "b", "c", "d"],
                [{"key": "value1"}, {"key": "value2"}],
            ],
        )
        def test_get_items_with_various_item_types(self, foreach_step_with_items, items):
            """Test that _get_items handles various types of items correctly."""
            data = {"items": items}
            result = foreach_step_with_items._get_items(data)
            assert list(result) == items

    class TestProcessStep:
        """
        Test class for the _process_step method of ForEachStep.

        This class contains tests for processing data through the foreach loop.
        """

        @patch("ai_graph.step.foreach.tqdm")
        def test_process_step_with_items_no_sub_steps(self, mock_tqdm, foreach_step_with_items):
            """Test that _process_step processes items correctly when no sub-steps are configured."""
            # Mock tqdm to return the enumerated items as expected
            mock_tqdm.return_value = [(0, 1), (1, 2), (2, 3)]
            data = {"items": [1, 2, 3]}

            result = foreach_step_with_items._process_step(data)

            assert len(result["results"]) == 3
            assert result["results"][0]["_current_item"] == 1
            assert result["results"][1]["_current_item"] == 2
            assert result["results"][2]["_current_item"] == 3
            assert result["results"][0]["_iteration_index"] == 0
            assert result["results"][1]["_iteration_index"] == 1
            assert result["results"][2]["_iteration_index"] == 2
            assert "items" in result  # Original data should be preserved

        @patch("ai_graph.step.foreach.tqdm")
        def test_process_step_with_items_and_sub_steps(self, mock_tqdm, foreach_step_with_items, mock_sub_step):
            """Test that _process_step processes items through sub-pipeline correctly."""
            # Setup mock tqdm to return enumerated items
            mock_tqdm.return_value = [(0, 10), (1, 20), (2, 30)]

            # Add sub-step and configure its behavior
            foreach_step_with_items.add_sub_step(mock_sub_step)
            foreach_step_with_items.sub_pipeline.process = MagicMock(
                side_effect=[
                    {"processed": "item1", "_current_item": 10, "_iteration_index": 0},
                    {"processed": "item2", "_current_item": 20, "_iteration_index": 1},
                    {"processed": "item3", "_current_item": 30, "_iteration_index": 2},
                ]
            )

            data = {"items": [10, 20, 30]}
            result = foreach_step_with_items._process_step(data)

            assert len(result["results"]) == 3
            assert result["results"][0]["processed"] == "item1"
            assert result["results"][1]["processed"] == "item2"
            assert result["results"][2]["processed"] == "item3"

        @patch("ai_graph.step.foreach.tqdm")
        def test_process_step_with_iterations(self, mock_tqdm, foreach_step_with_iterations, mock_sub_step):
            """Test that _process_step processes iterations correctly."""
            mock_tqdm.return_value = [(0, 0), (1, 1), (2, 2)]

            foreach_step_with_iterations.add_sub_step(mock_sub_step)
            foreach_step_with_iterations.sub_pipeline.process = MagicMock(
                side_effect=[
                    {"iteration": 0, "_current_item": 0, "_iteration_index": 0},
                    {"iteration": 1, "_current_item": 1, "_iteration_index": 1},
                    {"iteration": 2, "_current_item": 2, "_iteration_index": 2},
                ]
            )

            data = {"input": "data"}
            result = foreach_step_with_iterations._process_step(data)

            assert len(result["results"]) == 3
            assert result["results"][0]["iteration"] == 0
            assert result["results"][1]["iteration"] == 1
            assert result["results"][2]["iteration"] == 2

        @patch("ai_graph.step.foreach.tqdm")
        def test_process_step_iteration_context(self, mock_tqdm, foreach_step_with_items, mock_sub_step):
            """Test that _process_step creates correct iteration context for sub-pipeline."""
            mock_tqdm.return_value = [(0, "a"), (1, "b")]

            foreach_step_with_items.add_sub_step(mock_sub_step)

            # Capture the data passed to sub-pipeline
            captured_data = []

            def capture_process(data):
                captured_data.append(data.copy())
                return {"result": "processed"}

            foreach_step_with_items.sub_pipeline.process = MagicMock(side_effect=capture_process)

            data = {"items": ["a", "b"], "original": "data"}
            foreach_step_with_items._process_step(data)

            # Check first iteration context
            assert captured_data[0]["_current_item"] == "a"
            assert captured_data[0]["_iteration_index"] == 0
            assert captured_data[0]["original"] == "data"

            # Check second iteration context
            assert captured_data[1]["_current_item"] == "b"
            assert captured_data[1]["_iteration_index"] == 1
            assert captured_data[1]["original"] == "data"

        @patch("ai_graph.step.foreach.tqdm")
        def test_process_step_custom_results_key(self, mock_tqdm, mock_sub_step):
            """Test that _process_step uses custom results key correctly."""
            mock_tqdm.return_value = [(0, 1), (1, 2)]

            step = ForEachStep(items_key="items", results_key="custom_results")
            step.add_sub_step(mock_sub_step)
            step.sub_pipeline.process = MagicMock(return_value={"processed": True})

            data = {"items": [1, 2]}
            result = step._process_step(data)

            assert "custom_results" in result
            assert len(result["custom_results"]) == 2

        @patch("ai_graph.step.foreach.tqdm")
        def test_process_step_preserves_original_data(self, mock_tqdm, foreach_step_with_items):
            """Test that _process_step preserves original data in the result."""
            mock_tqdm.return_value = []

            data = {"items": [], "preserve": "this", "and": "this too"}
            result = foreach_step_with_items._process_step(data)

            assert result["preserve"] == "this"
            assert result["and"] == "this too"
            assert result["results"] == []

        @patch("ai_graph.step.foreach.tqdm")
        def test_process_step_with_non_iterable_items(self, mock_tqdm, foreach_step_with_items):
            """Test that _process_step handles non-iterable items correctly."""
            mock_tqdm.return_value = [(0, "single_item")]

            data = {"items": MagicMock(spec=int)}
            result = foreach_step_with_items._process_step(data)

            print(result)
            assert len(result["results"]) == 1
            assert "_current_item" in result["results"][0]
            assert result["results"][0]["_current_item"] == "single_item"

        @patch("ai_graph.step.foreach.tqdm")
        def test_process_step_with_non_sized_items(self, mock_tqdm, foreach_step_with_items):
            """Test that _process_step handles non-sized items correctly."""
            mock_tqdm.return_value = [(0, "item")]

            data = {"items": MagicMock(spec=list)}
            data["items"].__len__.side_effect = TypeError("Not iterable")
            data["items"].__iter__.return_value = iter(["item"])
            result = foreach_step_with_items._process_step(data)

            # assert len(result["results"]) == 1
            assert "_current_item" in result["results"][0]
            assert result["results"][0]["_current_item"] == "item"
            assert "items" in result
