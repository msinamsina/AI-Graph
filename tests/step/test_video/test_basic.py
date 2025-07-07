"""Tests for the basic video steps in the AI Graph pipeline."""

from unittest.mock import MagicMock, patch

import cv2
import numpy as np
import pytest

from ai_graph.step.video.basic import (
    OpenVideoCaptureStep,
    ReadFrameFromFileStep,
    ReadVideoFrameStep,
    ReleaseVideoCaptureStep,
    ReleaseVideoFrameStep,
)


class TestOpenVideoCaptureStep:
    """
    Test class for OpenVideoCaptureStep.

    This class contains tests for the OpenVideoCaptureStep class,
    which opens a video capture device or file.
    """

    class TestDunderInit:
        """
        Test class for the __init__ method of OpenVideoCaptureStep.

        This class contains tests for the initialization of the OpenVideoCaptureStep class.
        """

        def test_init_with_device_index(self):
            """Test that the __init__ method initializes the step correctly with device index."""
            step = OpenVideoCaptureStep(0)
            assert step.name == "OpenVideoCapture"
            assert step.source == 0

        def test_init_with_file_path(self):
            """Test that the __init__ method initializes the step correctly with file path."""
            step = OpenVideoCaptureStep("video.mp4")
            assert step.name == "OpenVideoCapture"
            assert step.source == "video.mp4"

        def test_init_with_custom_name(self):
            """Test that the __init__ method initializes the step correctly with custom name."""
            step = OpenVideoCaptureStep(0, name="CustomVideoCapture")
            assert step.name == "CustomVideoCapture"
            assert step.source == 0

    class TestUnderlineProcessStep:
        """
        Test class for the _process_step method of OpenVideoCaptureStep.

        This class contains tests for processing data by opening video capture.
        """

        @patch("cv2.VideoCapture")
        def test_process_step_success_with_file(self, mock_video_capture):
            """Test that the _process_step method successfully opens a video file."""
            # Mock the VideoCapture object
            mock_cap = MagicMock()
            mock_cap.isOpened.return_value = True
            mock_cap.get.side_effect = lambda prop: {
                cv2.CAP_PROP_FRAME_COUNT: 100,
                cv2.CAP_PROP_FPS: 30.0,
                cv2.CAP_PROP_FRAME_WIDTH: 1920,
                cv2.CAP_PROP_FRAME_HEIGHT: 1080,
                cv2.CAP_PROP_FOURCC: 1234567890,
            }.get(prop, 0)
            mock_video_capture.return_value = mock_cap

            step = OpenVideoCaptureStep("video.mp4")
            data = {}
            result = step._process_step(data)

            assert "video_capture" in result
            assert "capture" in result["video_capture"]
            assert "metadata" in result["video_capture"]

            metadata = result["video_capture"]["metadata"]
            assert metadata["frame_count"] == 100
            assert metadata["fps"] == 30.0
            assert metadata["width"] == 1920
            assert metadata["height"] == 1080
            assert metadata["fourcc"] == 1234567890
            assert metadata["is_file"] is True
            assert metadata["source"] == "video.mp4"

        @patch("cv2.VideoCapture")
        def test_process_step_success_with_device(self, mock_video_capture):
            """Test that the _process_step method successfully opens a video device."""
            mock_cap = MagicMock()
            mock_cap.isOpened.return_value = True
            mock_cap.get.side_effect = lambda prop: {
                cv2.CAP_PROP_FRAME_COUNT: 0,
                cv2.CAP_PROP_FPS: 30.0,
                cv2.CAP_PROP_FRAME_WIDTH: 640,
                cv2.CAP_PROP_FRAME_HEIGHT: 480,
                cv2.CAP_PROP_FOURCC: 0,
            }.get(prop, 0)
            mock_video_capture.return_value = mock_cap

            step = OpenVideoCaptureStep(0)
            data = {}
            result = step._process_step(data)

            assert "video_capture" in result
            metadata = result["video_capture"]["metadata"]
            assert metadata["is_file"] is False
            assert metadata["source"] == 0

        @patch("cv2.VideoCapture")
        def test_process_step_failure_cannot_open(self, mock_video_capture):
            """Test that the _process_step method raises ValueError when video cannot be opened."""
            mock_cap = MagicMock()
            mock_cap.isOpened.return_value = False
            mock_video_capture.return_value = mock_cap

            step = OpenVideoCaptureStep("nonexistent.mp4")
            data = {}

            with pytest.raises(ValueError, match="Could not open video source: nonexistent.mp4"):
                step._process_step(data)


class TestReadVideoFrameStep:
    """
    Test class for ReadVideoFrameStep.

    This class contains tests for the ReadVideoFrameStep class,
    which reads frames from a video capture device.
    """

    class TestDunderInit:
        """
        Test class for the __init__ method of ReadVideoFrameStep.

        This class contains tests for the initialization of the ReadVideoFrameStep class.
        """

        def test_init_default_name(self):
            """Test that the __init__ method initializes the step correctly with default name."""
            step = ReadVideoFrameStep()
            assert step.name == "ReadVideoFrame"

        def test_init_custom_name(self):
            """Test that the __init__ method initializes the step correctly with custom name."""
            step = ReadVideoFrameStep(name="CustomReadFrame")
            assert step.name == "CustomReadFrame"

    class TestUnderlineProcessStep:
        """
        Test class for the _process_step method of ReadVideoFrameStep.

        This class contains tests for processing data by reading video frames.
        """

        def test_process_step_success_with_dict_capture(self):
            """Test that the _process_step method successfully reads a frame from dict-style capture."""
            mock_cap = MagicMock()
            mock_cap.isOpened.return_value = True
            mock_cap.get.side_effect = lambda prop: {
                cv2.CAP_PROP_POS_FRAMES: 5,
                cv2.CAP_PROP_POS_MSEC: 1000.0,
            }.get(prop, 0)
            mock_cap.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))

            step = ReadVideoFrameStep()
            data = {"video_capture": {"capture": mock_cap, "metadata": {"is_file": False}}}
            result = step._process_step(data)

            assert "frame" in result
            assert "frame_num" in result
            assert "timestamp-ms" in result
            assert result["frame_num"] == 5
            assert result["timestamp-ms"] == 1000.0

        def test_process_step_success_with_direct_capture(self):
            """Test that the _process_step method successfully reads a frame from direct capture."""
            mock_cap = MagicMock()
            mock_cap.isOpened.return_value = True
            mock_cap.get.side_effect = lambda prop: {
                cv2.CAP_PROP_POS_FRAMES: 10,
                cv2.CAP_PROP_POS_MSEC: 2000.0,
            }.get(prop, 0)
            mock_cap.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))

            step = ReadVideoFrameStep()
            data = {"video_capture": mock_cap}
            result = step._process_step(data)

            assert "frame" in result
            assert result["frame_num"] == 10

        def test_process_step_with_specific_frame_number(self):
            """Test that the _process_step method seeks to specific frame number for files."""
            mock_cap = MagicMock()
            mock_cap.isOpened.return_value = True
            mock_cap.get.side_effect = lambda prop: {
                cv2.CAP_PROP_POS_FRAMES: 50,
                cv2.CAP_PROP_POS_MSEC: 5000.0,
            }.get(prop, 0)
            mock_cap.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))

            step = ReadVideoFrameStep()
            data = {"video_capture": {"capture": mock_cap, "metadata": {"is_file": True}}, "frame_num": 50}
            result = step._process_step(data)

            mock_cap.set.assert_called_once_with(cv2.CAP_PROP_POS_FRAMES, 50.0)
            assert result["frame_num"] == 50

        def test_process_step_failure_no_capture(self):
            """Test that the _process_step method raises ValueError when no capture is provided."""
            step = ReadVideoFrameStep()
            data = {}

            with pytest.raises(ValueError, match="Video capture is not initialized or opened."):
                step._process_step(data)

        def test_process_step_failure_capture_not_opened(self):
            """Test that the _process_step method raises ValueError when capture is not opened."""
            mock_cap = MagicMock()
            mock_cap.isOpened.return_value = False

            step = ReadVideoFrameStep()
            data = {"video_capture": mock_cap}

            with pytest.raises(ValueError, match="Video capture is not initialized or opened."):
                step._process_step(data)

        def test_process_step_failure_read_frame_fails(self):
            """Test that the _process_step method raises ValueError when frame reading fails."""
            mock_cap = MagicMock()
            mock_cap.isOpened.return_value = True
            mock_cap.read.return_value = (False, None)

            step = ReadVideoFrameStep()
            data = {"video_capture": mock_cap}

            with pytest.raises(ValueError, match="Failed to read frame from video capture."):
                step._process_step(data)


class TestReleaseVideoFrameStep:
    """
    Test class for ReleaseVideoFrameStep.

    This class contains tests for the ReleaseVideoFrameStep class,
    which releases the current video frame.
    """

    class TestDunderInit:
        """
        Test class for the __init__ method of ReleaseVideoFrameStep.

        This class contains tests for the initialization of the ReleaseVideoFrameStep class.
        """

        def test_init_default_name(self):
            """Test that the __init__ method initializes the step correctly with default name."""
            step = ReleaseVideoFrameStep()
            assert step.name == "ReleaseVideoFrame"

        def test_init_custom_name(self):
            """Test that the __init__ method initializes the step correctly with custom name."""
            step = ReleaseVideoFrameStep(name="CustomReleaseFrame")
            assert step.name == "CustomReleaseFrame"

    class TestUnderlineProcessStep:
        """
        Test class for the _process_step method of ReleaseVideoFrameStep.

        This class contains tests for processing data by releasing video frames.
        """

        @patch("builtins.print")
        def test_process_step_with_frame(self, mock_print):
            """Test that the _process_step method successfully releases a frame."""
            step = ReleaseVideoFrameStep()
            data = {"frame": np.zeros((480, 640, 3), dtype=np.uint8), "other_key": "value"}
            result = step._process_step(data)

            assert "frame" not in result
            assert "other_key" in result
            assert result["other_key"] == "value"
            mock_print.assert_not_called()

        @patch("builtins.print")
        def test_process_step_without_frame(self, mock_print):
            """Test that the _process_step method handles missing frame gracefully."""
            step = ReleaseVideoFrameStep()
            data = {"other_key": "value"}
            result = step._process_step(data)

            assert "frame" not in result
            assert "other_key" in result
            mock_print.assert_called_once_with("No frame to release.")


class TestReadFrameFromFileStep:
    """
    Test class for ReadFrameFromFileStep.

    This class contains tests for the ReadFrameFromFileStep class,
    which reads frames from image files.
    """

    class TestDunderInit:
        """
        Test class for the __init__ method of ReadFrameFromFileStep.

        This class contains tests for the initialization of the ReadFrameFromFileStep class.
        """

        def test_init_default_name(self):
            """Test that the __init__ method initializes the step correctly with default name."""
            step = ReadFrameFromFileStep()
            assert step.name == "ReadFrameFromFile"

        def test_init_custom_name(self):
            """Test that the __init__ method initializes the step correctly with custom name."""
            step = ReadFrameFromFileStep(name="CustomReadFromFile")
            assert step.name == "CustomReadFromFile"

    class TestUnderlineProcessStep:
        """
        Test class for the _process_step method of ReadFrameFromFileStep.

        This class contains tests for processing data by reading frames from files.
        """

        @patch("cv2.imread")
        def test_process_step_success(self, mock_imread):
            """Test that the _process_step method successfully reads a frame from file."""
            mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            mock_imread.return_value = mock_frame

            step = ReadFrameFromFileStep()
            data = {"frame_path": "/path/to/image.jpg"}
            result = step._process_step(data)

            assert "frame" in result
            assert np.array_equal(result["frame"], mock_frame)
            mock_imread.assert_called_once_with("/path/to/image.jpg")

        def test_process_step_failure_no_path(self):
            """Test that the _process_step method raises ValueError when no frame path is provided."""
            step = ReadFrameFromFileStep()
            data = {}

            with pytest.raises(ValueError, match="No frame path provided in data."):
                step._process_step(data)

        @pytest.mark.parametrize("invalid_path", [123, [], {}, None])
        def test_process_step_failure_invalid_path_type(self, invalid_path):
            """Test that the _process_step method raises ValueError for invalid path types."""
            step = ReadFrameFromFileStep()
            data = {"frame_path": invalid_path}

            with pytest.raises(ValueError, match=f"Frame path must be a string, got {type(invalid_path)}"):
                step._process_step(data)

        @patch("cv2.imread")
        def test_process_step_failure_imread_returns_none(self, mock_imread):
            """Test that the _process_step method raises ValueError when imread returns None."""
            mock_imread.return_value = None

            step = ReadFrameFromFileStep()
            data = {"frame_path": "/path/to/nonexistent.jpg"}

            with pytest.raises(ValueError, match="Failed to read frame from path: /path/to/nonexistent.jpg"):
                step._process_step(data)


class TestReleaseVideoCaptureStep:
    """
    Test class for ReleaseVideoCaptureStep.

    This class contains tests for the ReleaseVideoCaptureStep class,
    which releases the video capture device.
    """

    class TestDunderInit:
        """
        Test class for the __init__ method of ReleaseVideoCaptureStep.

        This class contains tests for the initialization of the ReleaseVideoCaptureStep class.
        """

        def test_init_default_name(self):
            """Test that the __init__ method initializes the step correctly with default name."""
            step = ReleaseVideoCaptureStep()
            assert step.name == "ReleaseVideoCapture"

        def test_init_custom_name(self):
            """Test that the __init__ method initializes the step correctly with custom name."""
            step = ReleaseVideoCaptureStep(name="CustomReleaseCapture")
            assert step.name == "CustomReleaseCapture"

    class TestUnderlineProcessStep:
        """
        Test class for the _process_step method of ReleaseVideoCaptureStep.

        This class contains tests for processing data by releasing video capture.
        """

        @patch("builtins.print")
        def test_process_step_with_opened_capture(self, mock_print):
            """Test that the _process_step method successfully releases an opened video capture."""
            mock_cap = MagicMock()
            mock_cap.isOpened.return_value = True

            step = ReleaseVideoCaptureStep()
            data = {"video_capture": mock_cap, "other_key": "value"}
            result = step._process_step(data)

            assert "video_capture" not in result
            assert "other_key" in result
            mock_cap.release.assert_called_once()
            mock_print.assert_not_called()

        @patch("builtins.print")
        def test_process_step_with_closed_capture(self, mock_print):
            """Test that the _process_step method handles closed video capture gracefully."""
            mock_cap = MagicMock()
            mock_cap.isOpened.return_value = False

            step = ReleaseVideoCaptureStep()
            data = {"video_capture": mock_cap, "other_key": "value"}
            result = step._process_step(data)

            assert "video_capture" in result  # Should not be deleted
            assert "other_key" in result
            mock_cap.release.assert_not_called()
            mock_print.assert_called_once_with("No video capture to release.")

        @patch("builtins.print")
        def test_process_step_without_capture(self, mock_print):
            """Test that the _process_step method handles missing video capture gracefully."""
            step = ReleaseVideoCaptureStep()
            data = {"other_key": "value"}
            result = step._process_step(data)

            assert "video_capture" not in result
            assert "other_key" in result
            mock_print.assert_called_once_with("No video capture to release.")

        @patch("builtins.print")
        def test_process_step_with_none_capture(self, mock_print):
            """Test that the _process_step method handles None video capture gracefully."""
            step = ReleaseVideoCaptureStep()
            data = {"video_capture": None, "other_key": "value"}
            result = step._process_step(data)

            assert "video_capture" in result  # Should not be deleted
            assert "other_key" in result
            mock_print.assert_called_once_with("No video capture to release.")
