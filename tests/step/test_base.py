"""Tests for the BasePipelineStep, AddKeyStep, and DelKeyStep classes in the AI Graph framework."""

from unittest.mock import MagicMock

import pytest

from ai_graph.step.base import AddKeyStep, BasePipelineStep, DelKeyStep


class TestBasePipelineStep:
    """
    Test class for BasePipelineStep.

    This class contains tests for the BasePipelineStep class,
    which is a base class for pipeline steps in the AI Graph framework.
    """

    @pytest.fixture
    def base_step(self):
        """Fixture that provides a basic BasePipelineStep instance for testing."""

        class BasePipelineStepTest(BasePipelineStep):
            """
            Test class for BasePipelineStep.

            This class is used to create an instance of BasePipelineStep for testing purposes.
            """

            def _process_step(self, data):
                return super()._process_step(data)

        return BasePipelineStepTest()

    class TestDunderInit:
        """
        Test class for the __init__ method of BasePipelineStep.

        This class contains tests for the initialization of the BasePipelineStep class.
        """

        def test_init(self, base_step):
            """Test that the __init__ method initializes the step correctly."""
            assert base_step is not None
            assert base_step.name == "BasePipelineStepTest"
            assert base_step._next_step is None

    class TestSetNext:
        """
        Test class for the set_next method of BasePipelineStep.

        This class contains tests for setting the next step in the pipeline.
        """

        def test_set_next(self, base_step):
            """Test that the set_next method sets the next step correctly."""
            next_step = MagicMock(spec=BasePipelineStep)
            base_step.set_next(next_step)
            assert base_step._next_step == next_step

    class TestProcess:
        """
        Test class for the process method of BasePipelineStep.

        This class contains tests for processing data through the pipeline step.
        """

        def test_process(self, base_step):
            """Test that the process method processes data correctly."""
            data = MagicMock(spec=dict)
            base_step._process_step = MagicMock(return_value=data)
            result = base_step.process(data)
            assert result == data
            base_step._process_step.assert_called_once_with(data)

        def test_process_with_next_step(self, base_step):
            """Test that the process method processes data through the next step in the pipeline."""
            next_step = MagicMock(spec=BasePipelineStep)
            base_step.set_next(next_step)

            data = MagicMock(spec=dict)
            base_step._process_step = MagicMock(return_value=data)
            next_step.process = MagicMock(return_value=data)

            result = base_step.process(data)
            assert result == data
            base_step._process_step.assert_called_once_with(data)
            next_step.process.assert_called_once_with(data)


class TestAddKeyStep:
    """Test class for the AddKeyStep class."""

    class TestDunderInit:
        """
        Test class for the __init__ method of AddKeyStep.

        This class contains tests for the initialization of the AddKeyStep class.
        """

        def test_init(self):
            """Test that the __init__ method initializes the step correctly."""
            step = AddKeyStep("test_key", "test_value")
            assert step.name == "AddKeyStep"
            assert step._key == "test_key"
            assert step._value == "test_value"

    class TestUnderlineProcessStep:
        """
        Test class for the _process_step method of AddKeyStep.

        This class contains tests for processing data by adding a key-value pair.
        """

        @pytest.mark.parametrize("data", [{}, {"existing_key": "existing_value"}, {"test_key": "old_value"}])
        def test_process_step(self, data):
            """Test that the _process_step method adds the key-value pair to the data."""
            step = AddKeyStep("test_key", "test_value")
            result = step._process_step(data)
            assert result == {**data, "test_key": "test_value"}


class TestDelKeyStep:
    """Test class for the DelKeyStep class."""

    class TestDunderInit:
        """
        Test class for the __init__ method of DelKeyStep.

        This class contains tests for the initialization of the DelKeyStep class.
        """

        def test_init(self):
            """Test that the __init__ method initializes the step correctly."""
            step = DelKeyStep("test_key")
            assert step.name == "DelKeyStep"
            assert step._key == "test_key"

    class TestUnderlineProcessStep:
        """
        Test class for the _process_step method of DelKeyStep.

        This class contains tests for processing data by deleting a key.
        """

        @pytest.mark.parametrize(
            "data, expected",
            [
                ({"test_key": "test_value"}, {}),
                ({"another_key": "another_value"}, {"another_key": "another_value"}),
                ({}, {}),
            ],
        )
        def test_process_step(self, data, expected):
            """Test that the _process_step method deletes the key from the data."""
            step = DelKeyStep("test_key")
            result = step._process_step(data)
            assert result == expected
