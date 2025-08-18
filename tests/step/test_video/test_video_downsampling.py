import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import cv2
import numpy as np
import pytest

# Import the class to be tested
from ai_graph.step.video.video_downsampling import VideoDownsamplingStep


# Mock torch.cuda.is_available globally for consistent testing environment
# We'll control this in specific tests if needed
@pytest.fixture(autouse=True)
def mock_cuda_availability():
    with patch("torch.cuda.is_available", return_value=False) as mock_is_available:
        yield mock_is_available


@pytest.fixture
def create_dummy_video():
    """Fixture to create a dummy video file for testing."""
    temp_dir = tempfile.mkdtemp()
    video_path = os.path.join(temp_dir, "dummy_video.mp4")

    # Create a simple dummy video using OpenCV
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec for .mp4
    fps = 10
    width, height = 640, 480
    out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

    for _ in range(fps * 2):  # 2 seconds of video
        frame = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
        out.write(frame)
    out.release()

    yield video_path

    # Clean up the dummy video file and directory
    os.remove(video_path)
    os.rmdir(temp_dir)


class TestVideoDownsamplingStep:
    class TestDunderInit:
        def test_init_default_parameters(self):
            step = VideoDownsamplingStep()
            assert step.name == "VideoDownsampling"
            assert step.output_fps == 5
            assert step.output_resolution is None
            assert step.output_format is None

        def test_init_custom_parameters(self):
            step = VideoDownsamplingStep(
                output_fps=10, output_resolution="1920x1080", output_format="webm", name="CustomDownsample"
            )
            assert step.name == "CustomDownsample"
            assert step.output_fps == 10
            assert step.output_resolution == "1920x1080"
            assert step.output_format == "webm"

    class TestUnderlineProcessStep:
        @pytest.fixture(autouse=True)
        def setup_mocks(self):
            # Mock os.path.isfile
            with patch("os.path.isfile", return_value=True) as mock_isfile:
                self.mock_isfile = mock_isfile
                # Mock cv2.VideoCapture
                with patch("cv2.VideoCapture") as mock_video_capture:
                    self.mock_cap = MagicMock()
                    self.mock_cap.isOpened.return_value = True
                    self.mock_cap.get.side_effect = lambda prop: {
                        cv2.CAP_PROP_FPS: 30.0,
                        cv2.CAP_PROP_FRAME_WIDTH: 1920,
                        cv2.CAP_PROP_FRAME_HEIGHT: 1080,
                    }.get(prop, 0)
                    mock_video_capture.return_value = self.mock_cap
                    # Mock subprocess.run
                    with patch("subprocess.run") as mock_subprocess_run:
                        self.mock_subprocess_run = mock_subprocess_run
                        self.mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="success", stderr="")
                        yield

        def test_process_step_raises_file_not_found_error_if_video_path_invalid(self):
            self.mock_isfile.return_value = False
            step = VideoDownsamplingStep()
            data = {"video_path": "/path/to/nonexistent.mp4"}
            with pytest.raises(FileNotFoundError, match="Invalid video path"):
                step._process_step(data)

        def test_process_step_raises_runtime_error_if_video_capture_fails_to_open(self):
            self.mock_cap.isOpened.return_value = False
            step = VideoDownsamplingStep()
            data = {"video_path": "/path/to/video.mp4"}
            with pytest.raises(RuntimeError, match="Failed to open video"):
                step._process_step(data)

        def test_process_step_skips_downsampling_if_output_fps_matches_original(self):
            self.mock_cap.get.side_effect = lambda prop: {cv2.CAP_PROP_FPS: 30.0}.get(prop, 0)
            step = VideoDownsamplingStep(output_fps=30)
            data = {"video_path": "/path/to/video.mp4"}

            result = step._process_step(data)

            self.mock_subprocess_run.assert_not_called()  # Assert ffmpeg was not called
            assert result["output_fps"] == 30
            assert result["video_fps"] == 30.0
            assert "video_path" in result  # Original video path should still be there
            assert result["video_path"] == "/path/to/video.mp4"  # Should not be changed

        @pytest.mark.parametrize(
            "output_fps, output_resolution, output_format, expected_vf_param, "
            "expected_codec_cpu, expected_codec_gpu, expected_suffix",
            [
                (15, None, None, '-vf "fps=15"', "libx264", "h264_nvenc", ".mp4"),
                (None, "1280x720", None, '-vf "scale=1280x720"', "libx264", "h264_nvenc", ".mp4"),
                (None, None, "webm", "", "libvpx-vp9", "libvpx-vp9", ".webm"),
                (10, "640x480", "mp4", '-vf "fps=10,scale=640x480"', "libx264", "h264_nvenc", ".mp4"),
                (5, "1920x1080", "webm", '-vf "fps=5,scale=1920x1080"', "libvpx-vp9", "libvpx-vp9", ".webm"),
            ],
        )
        def test_process_step_happy_path_generates_correct_ffmpeg_command_and_updates_data(
            self,
            output_fps,
            output_resolution,
            output_format,
            expected_vf_param,
            expected_codec_cpu,
            expected_codec_gpu,
            expected_suffix,
            mock_cuda_availability,
        ):
            # Arrange
            original_video_path = "/path/to/original_video.mp4"
            original_fps = 30.0
            self.mock_cap.get.side_effect = lambda prop: {cv2.CAP_PROP_FPS: original_fps}.get(prop, 0)

            step = VideoDownsamplingStep(
                output_fps=output_fps, output_resolution=output_resolution, output_format=output_format
            )
            data = {"video_path": original_video_path}

            # Mock Path.with_name to control the output filename
            mock_path_obj = MagicMock()
            mock_path_obj.stem = "original_video"
            mock_path_obj.suffix = ".mp4"
            expected_output_stem = mock_path_obj.stem + "_downsampled"
            expected_output_filename = expected_output_stem + expected_suffix
            expected_output_path = f"/path/to/{expected_output_filename}"  # Use forward slashes
            mock_path_obj.with_name.return_value = Path(expected_output_path)

            with patch("pathlib.Path", return_value=mock_path_obj):
                # Act
                result = step._process_step(data)

                # Assert
                self.mock_subprocess_run.assert_called_once()
                called_cmd = self.mock_subprocess_run.call_args[0][0]

                # Check common parts of the command
                assert f'ffmpeg -i "{original_video_path}"' in called_cmd
                if expected_vf_param:  # Only include -vf if filters are present
                    assert expected_vf_param in called_cmd
                else:
                    assert "-vf" not in called_cmd  # Ensure -vf is not present when no filters

                # Check codec based on GPU availability
                if mock_cuda_availability.return_value:
                    assert f"-c:v {expected_codec_gpu}" in called_cmd
                else:
                    assert f"-c:v {expected_codec_cpu}" in called_cmd

                assert "-c:a copy -max_muxing_queue_size 9999 -y" in called_cmd
                assert f'"{expected_output_path}"' in called_cmd  # Use POSIX-style path

                # Verify data dictionary updates
                assert result["output_fps"] == output_fps
                assert result["output_resolution"] == output_resolution
                assert result["output_format"] == output_format
                assert result["video_fps"] == original_fps
                assert result["video_path"] == str(mock_path_obj.with_name.return_value)

        def test_process_step_raises_runtime_error_if_ffmpeg_fails(self):
            self.mock_subprocess_run.return_value = MagicMock(returncode=1, stdout="", stderr="FFmpeg error message")
            step = VideoDownsamplingStep(output_fps=15)
            data = {"video_path": "/path/to/video.mp4"}

            with pytest.raises(RuntimeError, match="FFmpeg failed with exit code 1"):
                step._process_step(data)

        def test_process_step_uses_gpu_acceleration_when_available(self, mock_cuda_availability):
            mock_cuda_availability.return_value = True  # Simulate GPU available
            step = VideoDownsamplingStep(output_fps=15)
            data = {"video_path": "/path/to/video.mp4"}

            # Mock Path.with_name to control the output filename
            mock_path_obj = MagicMock()
            mock_path_obj.stem = "video"
            mock_path_obj.suffix = ".mp4"
            mock_path_obj.with_name.return_value = Path("/path/to/video_15fps.mp4")
            with patch("pathlib.Path", return_value=mock_path_obj):
                step._process_step(data)

            called_cmd = self.mock_subprocess_run.call_args[0][0]
            assert "-hwaccel cuda" in called_cmd
            assert "-c:v h264_nvenc" in called_cmd  # Default GPU codec for mp4

        def test_process_step_uses_cpu_when_gpu_not_available(self, mock_cuda_availability):
            mock_cuda_availability.return_value = False  # Simulate GPU not available (default)
            step = VideoDownsamplingStep(output_fps=15)
            data = {"video_path": "/path/to/video.mp4"}

            # Mock Path.with_name to control the output filename
            mock_path_obj = MagicMock()
            mock_path_obj.stem = "video"
            mock_path_obj.suffix = ".mp4"
            mock_path_obj.with_name.return_value = Path("/path/to/video_15fps.mp4")
            with patch("pathlib.Path", return_value=mock_path_obj):
                step._process_step(data)

            called_cmd = self.mock_subprocess_run.call_args[0][0]
            assert "-hwaccel cuda" not in called_cmd  # Should not use GPU accel
            assert "-c:v libx264" in called_cmd  # Default CPU codec for mp4

        def test_process_step_handles_missing_video_path_in_data(self):
            step = VideoDownsamplingStep()
            data = {}  # Missing video_path

            with pytest.raises(FileNotFoundError, match="Invalid video path"):
                step._process_step(data)
