import json
import os
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from ai_graph.step.video.video_downsampling import (
    VideoDownsamplingStep,
    check_ffmpeg_availability,
    install_ffmpeg,
)


@pytest.fixture
def mock_subprocess_run():
    """Fixture to mock subprocess.run for FFmpeg and FFprobe commands."""
    with patch("subprocess.run") as mock_run:
        yield mock_run


@pytest.fixture
def mock_path_isfile():
    """Fixture to mock os.path.isfile."""
    with patch("os.path.isfile") as mock_isfile:
        yield mock_isfile


@pytest.fixture
def video_downsampling_step():
    """Fixture to create a VideoDownsamplingStep instance."""
    return VideoDownsamplingStep(output_fps=10, output_resolution="640x480", output_format="mp4")


def test_check_ffmpeg_availability_success(mock_subprocess_run):
    """Test check_ffmpeg_availability when FFmpeg and FFprobe are available."""
    mock_subprocess_run.side_effect = [
        MagicMock(returncode=0),  # ffmpeg -version
        MagicMock(returncode=0),  # ffprobe -version
    ]
    ffmpeg_path, ffprobe_path = check_ffmpeg_availability()
    assert ffmpeg_path == "ffmpeg"
    assert ffprobe_path == "ffprobe"
    assert mock_subprocess_run.call_count == 2


def test_check_ffmpeg_availability_not_found(mock_subprocess_run):
    """Test check_ffmpeg_availability when FFmpeg/FFprobe are not found."""
    mock_subprocess_run.side_effect = FileNotFoundError
    with patch(
        "ai_graph.step.video.video_downsampling.install_ffmpeg",
        return_value=("/path/to/ffmpeg", "/path/to/ffprobe"),
    ) as mock_install:
        ffmpeg_path, ffprobe_path = check_ffmpeg_availability()
        assert ffmpeg_path == "/path/to/ffmpeg"
        assert ffprobe_path == "/path/to/ffprobe"
        mock_install.assert_called_once()


def test_install_ffmpeg_success(mock_subprocess_run):
    """Test install_ffmpeg when the command succeeds."""
    mock_subprocess_run.return_value = MagicMock(returncode=0)
    with patch("ai_graph.step.video.video_downsampling.ffdl") as mock_ffdl:
        mock_ffdl.ffmpeg_path = "/path/to/ffmpeg"
        mock_ffdl.ffprobe_path = "/path/to/ffprobe"
        ffmpeg_path, ffprobe_path = install_ffmpeg()
        assert ffmpeg_path == "/path/to/ffmpeg"
        assert ffprobe_path == "/path/to/ffprobe"
        mock_subprocess_run.assert_called_once_with(["ffdl", "install"], input=b"y\n", check=True)


def test_install_ffmpeg_file_not_found(mock_subprocess_run):
    """Test install_ffmpeg when ffdl command is not found."""
    mock_subprocess_run.side_effect = FileNotFoundError
    with pytest.raises(SystemExit):
        install_ffmpeg()


def test_install_ffmpeg_non_zero_exit(mock_subprocess_run):
    """Test install_ffmpeg when command returns non-zero exit code."""
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, ["ffdl", "install"])
    with pytest.raises(SystemExit):
        install_ffmpeg()


def test_video_downsampling_init():
    """Test initialization of VideoDownsamplingStep."""
    step = VideoDownsamplingStep(output_fps=15, output_resolution="1280x720", output_format="webm", name="TestStep")
    assert step.output_fps == 15
    assert step.output_resolution == "1280x720"
    assert step.output_format == "webm"
    assert step.name == "TestStep"


def test_get_video_fps_success(mock_subprocess_run, video_downsampling_step):
    """Test _get_video_fps when FFprobe returns valid FPS data."""
    # Reset mock to ignore calls from check_ffmpeg_availability
    mock_subprocess_run.reset_mock()
    mock_subprocess_run.return_value = MagicMock(
        returncode=0,
        stdout=json.dumps({"streams": [{"r_frame_rate": "30/1"}]}),
        stderr="",
    )
    fps = video_downsampling_step._get_video_fps("/path/to/video.mp4")
    assert fps == 30.0
    mock_subprocess_run.assert_called_once_with(
        f'"{video_downsampling_step.ffprobe_path}" -v error -select_streams v:0 -show_entries stream=r_frame_rate -of json "/path/to/video.mp4"',
        shell=True,
        capture_output=True,
        text=True,
    )


def test_get_video_fps_failure(mock_subprocess_run, video_downsampling_step):
    """Test _get_video_fps when FFprobe fails."""
    mock_subprocess_run.return_value = MagicMock(returncode=1, stderr="FFprobe error")
    with pytest.raises(RuntimeError, match="FFprobe failed to retrieve FPS"):
        video_downsampling_step._get_video_fps("/path/to/video.mp4")


def test_process_step_invalid_path(mock_path_isfile, video_downsampling_step):
    """Test _process_step with an invalid video path."""
    mock_path_isfile.return_value = False
    data = {"video_path": "/invalid/path/video.mp4"}
    with pytest.raises(FileNotFoundError, match="Invalid video path"):
        video_downsampling_step._process_step(data)


def test_process_step_same_fps(mock_path_isfile, mock_subprocess_run, video_downsampling_step):
    """Test _process_step when original and target FPS are the same."""
    mock_path_isfile.return_value = True
    mock_subprocess_run.return_value = MagicMock(
        returncode=0,
        stdout=json.dumps({"streams": [{"r_frame_rate": "10/1"}]}),
        stderr="",
    )
    data = {"video_path": "/path/to/video.mp4"}
    result = video_downsampling_step._process_step(data)
    assert result["video_path"] == "/path/to/video.mp4"
    assert result["output_fps"] == 10
    assert result["video_fps"] == 10.0
    assert result["output_resolution"] == "640x480"
    assert result["output_format"] == "mp4"


from pathlib import Path


def test_process_step_downsample(mock_path_isfile, mock_subprocess_run, video_downsampling_step):
    """Test _process_step with actual downsampling."""
    mock_path_isfile.return_value = True
    mock_subprocess_run.side_effect = [
        MagicMock(
            returncode=0,
            stdout=json.dumps({"streams": [{"r_frame_rate": "30/1"}]}),
            stderr="",
        ),  # FFprobe for FPS
        MagicMock(returncode=0, stdout="success", stderr=""),  # FFmpeg for downsampling
    ]
    data = {"video_path": "/path/to/video.mp4"}
    with patch.object(video_downsampling_step, "_downsample_video") as mock_downsample:
        result = video_downsampling_step._process_step(data)
        # Normalize the result path to use forward slashes for comparison
        assert Path(result["video_path"]).as_posix() == "/path/to/video_downsampled.mp4"
        assert result["output_fps"] == 10
        assert result["video_fps"] == 30.0
        assert result["output_resolution"] == "640x480"
        assert result["output_format"] == "mp4"
        mock_downsample.assert_called_once()


def test_downsample_video_cpu(mock_subprocess_run, video_downsampling_step):
    """Test _downsample_video using CPU encoding."""
    # Reset mock to ignore calls from check_ffmpeg_availability
    mock_subprocess_run.reset_mock()
    mock_subprocess_run.side_effect = [
        MagicMock(returncode=0, stdout="auto", stderr=""),  # FFmpeg -hwaccels
        MagicMock(returncode=0, stdout="success", stderr=""),  # FFmpeg downsample
    ]
    video_downsampling_step._downsample_video("/path/to/input.mp4", "/path/to/output.mp4", 10, "640x480", "mp4")
    assert mock_subprocess_run.call_count == 2
    cmd = mock_subprocess_run.call_args_list[1][0][0]
    assert "libx264" in cmd
    assert "fps=10" in cmd
    assert "scale=640x480" in cmd


def test_downsample_video_gpu(mock_subprocess_run, video_downsampling_step):
    """Test _downsample_video using GPU encoding."""
    mock_subprocess_run.reset_mock()
    mock_subprocess_run.side_effect = [
        MagicMock(returncode=0, stdout="cuda", stderr=""),  # FFmpeg -hwaccels
        MagicMock(returncode=0, stdout="success", stderr=""),  # FFmpeg downsample
    ]
    video_downsampling_step._downsample_video("/path/to/input.mp4", "/path/to/output.mp4", 10, "640x480", "mp4")
    assert mock_subprocess_run.call_count == 2
    cmd = mock_subprocess_run.call_args_list[1][0][0]
    assert "h264_nvenc" in cmd
    assert "fps=10" in cmd
    assert "scale=640x480" in cmd


def test_downsample_video_webm(mock_subprocess_run, video_downsampling_step):
    """Test _downsample_video with WebM format."""
    mock_subprocess_run.reset_mock()
    mock_subprocess_run.side_effect = [
        MagicMock(returncode=0, stdout="cuda", stderr=""),  # FFmpeg -hwaccels
        MagicMock(returncode=0, stdout="success", stderr=""),  # FFmpeg downsample
    ]
    video_downsampling_step._downsample_video("/path/to/input.mp4", "/path/to/output.webm", 10, "640x480", "webm")
    assert mock_subprocess_run.call_count == 2
    cmd = mock_subprocess_run.call_args_list[1][0][0]
    assert "libvpx-vp9" in cmd
    assert "fps=10" in cmd
    assert "scale=640x480" in cmd


def test_downsample_video_failure(mock_subprocess_run, video_downsampling_step):
    """Test _downsample_video when FFmpeg fails."""
    mock_subprocess_run.side_effect = [
        MagicMock(returncode=0, stdout="auto", stderr=""),  # FFmpeg -hwaccels
        subprocess.CalledProcessError(1, cmd="ffmpeg", stderr="FFmpeg error"),
    ]
    with pytest.raises(RuntimeError, match="FFmpeg failed"):
        video_downsampling_step._downsample_video("/path/to/input.mp4", "/path/to/output.mp4", 10, "640x480", "mp4")
