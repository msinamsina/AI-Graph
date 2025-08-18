"""
Video Downsampling Step.

This module provides a pipeline step for downsampling a video to a specified
frames-per-second (FPS) rate.
"""

import logging
import os
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, Optional

import cv2
import torch

from ..base import BasePipelineStep

logger = logging.getLogger(__name__)


class VideoDownsamplingStep(BasePipelineStep):
    """
    Pipeline step to downsample a video to a target FPS, resolution, and/or format.

    This step takes a video file path, processes it according to specified
    output parameters (FPS, resolution, format), and saves the output video
    next to the original file with a '_downsampled' suffix, along with
    resolution and FPS information if provided. It uses FFmpeg for the
    conversion and can leverage GPU acceleration (NVIDIA's NVENC) if a
    compatible GPU and CUDA are detected.

    Examples:
       # Example 1: Downsample to 15 FPS
       downsample_fps_step = VideoDownsamplingStep(output_fps=15)

       # Example 2: Downsample to 720p resolution
       downsample_res_step = VideoDownsamplingStep(output_resolution="1280x720")

       # Example 3: Convert to WebM format
       convert_format_step = VideoDownsamplingStep(output_format="webm")

       # Example 4: Downsample to 10 FPS, 480p resolution, and MP4 format
       full_downsample_step = VideoDownsamplingStep(
           output_fps=10,
           output_resolution="640x480",
           output_format="mp4"
       )
    """

    def __init__(
        self,
        output_fps: Optional[int] = 5,
        output_resolution: Optional[str] = None,
        output_format: Optional[str] = None,
        name: Optional[str] = None,
    ):
        """
        Initializes the VideoDownsamplingStep.

        Args:
            output_fps (int): The target frames-per-second for the output video.
            output_resolution (str, optional): The target resolution for the output video (e.g., "1280x720").
            output_format (str, optional): The target format for the output video (e.g., "mp4", "webm").
            name (str, optional): The name of the pipeline step. Defaults to "VideoDownsampling".

        Example:
            >>> step = VideoDownsamplingStep(output_fps=15, output_resolution="1280x720", output_format="mp4")
        """
        super().__init__(name or "VideoDownsampling")
        self.output_fps = output_fps
        self.output_resolution = output_resolution
        self.output_format = output_format

    def _process_step(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Downsamples the video specified in the input data.

        This method reads the 'video_path' from the input data, checks if the
        video needs downsampling, performs the downsampling using FFmpeg, and
        updates the 'video_path' in the data to point to the new downsampled file.

        Args:
            data (Dict[str, Any]): A dictionary containing the 'video_path' to the
                video file to be downsampled.

        Returns:
            Dict[str, Any]: The updated data dictionary with 'video_path' pointing
                to the processed video file if downsampling/conversion was performed.
                It also includes 'output_fps', 'output_resolution', 'output_format',
                and the original 'video_fps'.

        Raises:
            FileNotFoundError: If the video_path is not found or is invalid.
            RuntimeError: If FFmpeg fails to open or process the video.

        Example:
            >>> from ai_graph.step.video.video_downsampling import VideoDownsamplingStep
            >>> step = VideoDownsamplingStep(output_fps=10, output_resolution="640x480", output_format="mp4")
            >>> data = {"video_path": "/path/to/your/video.mp4"}
            >>> # For a runnable example, you would need to mock os.path.isfile, cv2.VideoCapture, and subprocess.run
            >>> # processed_data = step._process_step(data)
            >>> # print(processed_data["video_path"])
            # Expected output (if mocks were in place):
            # /path/to/your/video_downsampled_640x480_10fps.mp4
        """
        video_path = data.get("video_path")
        if not video_path or not os.path.isfile(video_path):
            raise FileNotFoundError(f"Invalid video path: {video_path}")

        # Get original fps
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise RuntimeError(f"Failed to open video: {video_path}")
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()

        logger.info(f"Original FPS: {original_fps:.2f}")
        logger.info(f"Target FPS: {self.output_fps}")

        if self.output_fps is not None and original_fps == self.output_fps:
            logger.info("Original FPS and Target FPS are the same. Skipping downsampling.")
            data["output_fps"] = self.output_fps
            data["video_fps"] = original_fps
            data["output_resolution"] = self.output_resolution
            data["output_format"] = self.output_format
            return data

        video_p = Path(video_path)

        # Construct output filename based on provided parameters
        output_stem = video_p.stem + "_downsampled"

        output_suffix = f".{self.output_format}" if self.output_format else video_p.suffix
        output_path = str(video_p.with_name(f"{output_stem}{output_suffix}"))

        start_time = time.time()
        try:
            self._downsample_video(video_path, output_path, self.output_fps, self.output_resolution, self.output_format)
            data["video_path"] = output_path
        except Exception as e:
            logger.error(f"Error downsampling video {video_path}: {e}")
            raise

        elapsed = time.time() - start_time
        logger.info(f"Downsampling took {elapsed:.2f} seconds")

        data["output_fps"] = self.output_fps
        data["video_fps"] = original_fps
        data["output_resolution"] = self.output_resolution
        data["output_format"] = self.output_format
        return data

    def _downsample_video(
        self,
        input_path: str,
        output_path: str,
        output_fps: Optional[int],
        output_resolution: Optional[str],
        output_format: Optional[str],
    ) -> None:
        """
        Performs the video downsampling using FFmpeg.

        This method constructs and executes an FFmpeg command to change the video's
        FPS and/or resolution. It automatically selects hardware acceleration (h264_nvenc) if a
        CUDA-enabled GPU is available, otherwise, it falls back to CPU-based
        encoding (libx264).

        Args:
            input_path (str): The path to the input video file.
            output_path (str): The path where the downsampled video will be saved.
            output_fps (Optional[int]): The target frames-per-second for the output video.
            output_resolution (Optional[str]): The target resolution for the output video (e.g., "1280x720").
            output_format (Optional[str]): The target format for the output video (e.g., "mp4", "webm").

        Raises:
            RuntimeError: If the FFmpeg command fails to execute.

        Example:
            >>> # This example assumes ffmpeg is installed and accessible in the system's PATH.
            >>> # It also assumes a dummy video file exists at '/tmp/input_video.mp4'.
            >>> # Mocking subprocess.run and torch.cuda.is_available would be necessary for a real test.
            >>> from pathlib import Path
            >>> from unittest.mock import patch, MagicMock
            >>> from ai_graph.step.video.video_downsampling import VideoDownsamplingStep
            >>>
            >>> # Mock subprocess.run to prevent actual ffmpeg execution during example run
            >>> with patch('subprocess.run', return_value=MagicMock(returncode=0, stdout="success", stderr="")):
            >>>     # Mock torch.cuda.is_available to simulate no GPU
            >>>     with patch('torch.cuda.is_available', return_value=False):
            >>>         step = VideoDownsamplingStep()
            >>>         # Instance is not used for _downsample_video directly, but for context
            >>>         input_path = "/tmp/input_video.mp4"
            >>>         output_path = "/tmp/output_video_downsampled.mp4"
            >>>         # Call the static method directly for demonstration
            >>>         VideoDownsamplingStep._downsample_video(step, input_path, output_path, 15, "640x480", "mp4")
            >>>         # In a real scenario, you would check if output_video_downsampled.mp4 was created.
        """
        try:
            use_gpu = torch.cuda.is_available()

            filters = []
            if output_fps is not None:
                filters.append(f"fps={output_fps}")
            if output_resolution is not None:
                filters.append(f"scale={output_resolution}")

            vf_param = f'-vf "{",".join(filters)}"' if filters else ""

            # Determine video codec based on format
            video_codec_gpu = "h264_nvenc"
            video_codec_cpu = "libx264"
            if output_format == "webm":
                video_codec_gpu = "libvpx-vp9"  # NVENC doesn't support VP9 directly, so fallback to CPU for webm
                video_codec_cpu = "libvpx-vp9"
            elif output_format == "mp4":
                video_codec_gpu = "h264_nvenc"
                video_codec_cpu = "libx264"
            # Add more format-codec mappings as needed

            # Ensure output_path uses POSIX-style separators for ffmpeg
            ffmpeg_output_path = Path(output_path).as_posix()

            if use_gpu:
                logger.info("GPU detected - using hardware acceleration for ffmpeg")
                cmd = (
                    f'ffmpeg -hwaccel cuda -i "{input_path}" {vf_param} '
                    f"-c:v {video_codec_gpu} -preset fast -c:a copy "
                    f'-max_muxing_queue_size 9999 -y "{ffmpeg_output_path}"'
                )
            else:
                logger.info("No GPU detected - using CPU for ffmpeg")
                cmd = (
                    f'ffmpeg -i "{input_path}" {vf_param} '
                    f"-c:v {video_codec_cpu} -preset fast -c:a copy "
                    f'-max_muxing_queue_size 9999 -y "{ffmpeg_output_path}"'
                )

            # Execute the ffmpeg command
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            # Check for errors
            if result.returncode != 0:
                logger.error(f"FFmpeg error: {result.stderr}")
                raise RuntimeError(f"FFmpeg failed with exit code {result.returncode}")
            else:
                logger.info(f"Successfully downsampled video to {output_path}")

        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg command failed: {e.stderr}")
            raise RuntimeError(f"FFmpeg failed: {e.stderr}") from e
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            raise
