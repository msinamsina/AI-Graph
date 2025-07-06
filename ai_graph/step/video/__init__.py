"""
Video Processing Steps Module.

This module provides comprehensive video processing steps for AI-Graph pipelines,
including opening video capture devices or files, reading frames, frame management,
and video-related utilities.

The module is built on top of OpenCV and provides a high-level interface for
video processing tasks in pipeline architectures.

Available Steps:
    OpenVideoCaptureStep: Opens video capture devices or files
    ReadVideoFrameStep: Reads frames from video capture objects
    ReadFrameFromFileStep: Reads individual frames from image files
    ReleaseVideoFrameStep: Releases current video frame from memory
    ReleaseVideoCaptureStep: Releases video capture resources

Example:
    >>> from ai_graph.step.video import OpenVideoCaptureStep, ReadVideoFrameStep
    >>> from ai_graph.pipeline import Pipeline
    >>>
    >>> # Create a pipeline to read frames from a video file
    >>> pipeline = Pipeline("VideoReader")
    >>> pipeline.add_step(OpenVideoCaptureStep("video.mp4"))
    >>> pipeline.add_step(ReadVideoFrameStep())
    >>>
    >>> # Process the pipeline
    >>> result = pipeline.process({})
    >>> frame = result['frame']  # numpy array containing the frame
"""
