"""
Video Processing Steps Module.

This module provides basic video processing steps for a pipeline,
including opening a video capture device or file, reading frames,
releasing frames, and reading frames from a file path.
"""

from typing import Any, Dict, Optional, Union

import cv2

from ..base import BasePipelineStep


class OpenVideoCaptureStep(BasePipelineStep):
    """Pipeline step to open a video capture device or file."""

    def __init__(self, source: Union[int, str], name: Optional[str] = None):
        """
        Initialize the video capture step.

        Args:
            source (int or str): Video source (device index or file path).
            name (str, optional): Name of this pipeline step.
        """
        super().__init__(name or "OpenVideoCapture")
        self.source = source

    def _process_step(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Open the video capture and return the capture object.

        This method opens a video capture device or file and extracts metadata
        including frame count, FPS, dimensions, and format information.

        Args:
            data (Dict[str, Any]): Input data dictionary.

        Returns:
            Dict[str, Any]: Updated data dictionary with video_capture containing:
                - capture: The OpenCV VideoCapture object
                - metadata: Dictionary with video properties (frame_count, fps, width, height, etc.)

        Raises:
            ValueError: If the video source cannot be opened.
        """
        cap = cv2.VideoCapture(self.source)
        if not cap.isOpened():
            raise ValueError(f"Could not open video source: {self.source}")

        metadata: Dict[str, Any] = {}
        # If source is a file, try to get metadata
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        metadata["frame_count"] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        metadata["fps"] = cap.get(cv2.CAP_PROP_FPS)
        metadata["width"] = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        metadata["height"] = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        metadata["fourcc"] = cap.get(cv2.CAP_PROP_FOURCC)
        metadata["is_file"] = isinstance(self.source, str) and self.source.endswith((".mp4", ".avi", ".mov", ".mkv"))
        metadata["source"] = self.source

        data["video_capture"] = {"capture": cap, "metadata": metadata}
        return data


class ReadVideoFrameStep(BasePipelineStep):
    """
    Pipeline step to read a frame from the video capture device.

    This step reads the next frame from an opened video capture device or file.
    It supports both sequential reading and seeking to specific frame numbers.

    Examples:
        >>> # Reading sequential frames
        >>> step = ReadVideoFrameStep()
        >>> data = {'video_capture': {'capture': cap, 'metadata': metadata}}
        >>> result = step.process(data)
        >>> frame = result['frame']

        >>> # Reading a specific frame
        >>> data = {'video_capture': {'capture': cap, 'metadata': metadata}, 'frame_num': 100}
        >>> result = step.process(data)
    """

    def __init__(self, name: Optional[str] = None):
        """
        Initialize the read step.

        Args:
            name (str, optional): Name of this pipeline step.
        """
        super().__init__(name or "ReadVideoFrame")

    def _process_step(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Read a frame from the video capture object.

        Args:
            data (Dict[str, Any]): Input data containing video_capture object.

        Returns:
            Dict[str, Any]: Dictionary containing:
                - frame: The read frame as a numpy array
                - frame_num: The frame number (int)
                - timestamp-ms: The timestamp in milliseconds

        Raises:
            ValueError: If video capture is not initialized, opened, or frame read fails.
        """
        cap_info = data.get("video_capture")
        cap: Optional[cv2.VideoCapture] = None
        cap_metadata: Optional[Dict[str, Any]] = None

        if isinstance(cap_info, dict):
            cap_metadata = cap_info.get("metadata")
            cap = cap_info.get("capture")
        else:
            cap = cap_info

        if not cap or not cap.isOpened():
            raise ValueError("Video capture is not initialized or opened.")

        frame_num: float
        if "frame_num" in data and cap_metadata and cap_metadata.get("is_file", False):
            frame_num = float(data["frame_num"])
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        else:
            frame_num = cap.get(cv2.CAP_PROP_POS_FRAMES)

        ret, frame = cap.read()
        if not ret:
            raise ValueError("Failed to read frame from video capture.")

        return {
            "frame": frame,
            "frame_num": int(frame_num),
            "timestamp-ms": cap.get(cv2.CAP_PROP_POS_MSEC),
        }


class ReleaseVideoFrameStep(BasePipelineStep):
    """Pipeline step to release the current video frame."""

    def __init__(self, name: Optional[str] = None):
        """
        Initialize the release step.

        Args:
            name (str, optional): Name of this pipeline step.
        """
        super().__init__(name or "ReleaseVideoFrame")

    def _process_step(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Release the current video frame if it exists."""
        if "frame" in data:
            del data["frame"]
        else:
            print("No frame to release.")
        return data


class ReadFrameFromFileStep(BasePipelineStep):
    """
    Pipeline step to read a frame from a file path.

    This step reads an image file from the filesystem using OpenCV's imread function.
    It supports all image formats supported by OpenCV including JPEG, PNG, BMP, TIFF, etc.

    Examples:
        >>> step = ReadFrameFromFileStep()
        >>> data = {'frame_path': '/path/to/image.jpg'}
        >>> result = step.process(data)
        >>> frame = result['frame']  # numpy array containing the image
    """

    def __init__(self, name: Optional[str] = None):
        """
        Initialize the read frame step.

        Args:
            name (str, optional): Name of this pipeline step.
        """
        super().__init__(name or "ReadFrameFromFile")

    def _process_step(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Read a frame from the specified file path.

        Args:
            data (Dict[str, Any]): Input data containing frame_path.

        Returns:
            Dict[str, Any]: Updated data dictionary with the loaded frame.

        Raises:
            ValueError: If no frame path is provided or frame reading fails.
        """
        if "frame_path" not in data:
            raise ValueError("No frame path provided in data.")

        frame_path = data["frame_path"]
        if not isinstance(frame_path, str):
            raise ValueError(f"Frame path must be a string, got {type(frame_path)}")

        frame = cv2.imread(frame_path)
        if frame is None:
            raise ValueError(f"Failed to read frame from path: {frame_path}")

        data["frame"] = frame
        return data


class ReleaseVideoCaptureStep(BasePipelineStep):
    """Pipeline step to release the video capture device."""

    def __init__(self, name: Optional[str] = None):
        """
        Initialize the release step.

        Args:
            name (str, optional): Name of this pipeline step.
        """
        super().__init__(name or "ReleaseVideoCapture")

    def _process_step(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Release the video capture object if it exists."""
        cap = data.get("video_capture")
        if cap and cap.isOpened():
            cap.release()
            del data["video_capture"]
        else:
            print("No video capture to release.")
        return data
