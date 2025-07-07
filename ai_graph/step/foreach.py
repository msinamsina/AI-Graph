"""ForEach pipeline implementation using Chain of Responsibility pattern."""

from typing import Any, Dict, Iterable, Optional

from tqdm import tqdm

from ..pipeline.base import Pipeline
from .base import BasePipelineStep


class ForEachStep(BasePipelineStep):
    """Pipeline step that processes each item in a collection or runs a fixed number of iterations.

    This step creates a sub-pipeline that processes each item or runs for each iteration.
    Results are collected in the output data.
    """

    def __init__(
        self,
        items_key: Optional[str] = None,
        iterations: Optional[int] = None,
        results_key: str = "foreach_results",
        name: Optional[str] = None,
    ):
        """Initialize a ForEach step.

        Args:
            items_key: Key in the input data containing the items to iterate over.
                       If None, uses the iterations parameter instead.
            iterations: Number of iterations to run if items_key is None.
            results_key: Key in output data where results will be stored.
            name: Name of this pipeline step.

        Raises:
            ValueError: If neither items_key nor iterations is provided.
        """
        super().__init__(name)
        if items_key is None and iterations is None:
            raise ValueError("Either items_key or iterations must be provided")

        self.items_key = items_key
        self.iterations = iterations
        self.results_key = results_key
        self.sub_pipeline = Pipeline(name=f"{self.name}_SubPipeline")

    def add_sub_step(self, step: BasePipelineStep) -> "ForEachStep":
        """Add a step to the sub-pipeline.

        Args:
            step: Step to add to the sub-pipeline.

        Returns:
            Self for method chaining.
        """
        self.sub_pipeline.add_step(step)
        return self

    def _get_items(self, data: Dict[str, Any]) -> Iterable[Any]:
        """Get items to iterate over from input data or generate range.

        Args:
            data: Input data dictionary.

        Returns:
            Iterable of items to process or range of iteration counts.
        """
        if self.items_key is not None and self.items_key in data:
            items = data[self.items_key]
            if hasattr(items, "__iter__") and not isinstance(items, str):
                return items  # type: ignore[no-any-return]
            else:
                return [items]  # Wrap single item in list
        return range(self.iterations or 0)

    def _process_step(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process each item in the collection or for each iteration.

        Args:
            data: Input data to be processed.

        Returns:
            Processed data with results from all iterations.
        """
        items = self._get_items(data)
        results = []

        # Calculate total for progress bar
        if self.items_key is None:
            total = self.iterations
        else:
            try:
                total = len(items)  # type: ignore
            except TypeError:
                # If items is not sized, we can't show progress
                total = None

        # print tqdm progress bar for the iterations and items
        for i, item in tqdm(
            enumerate(items),
            total=total,
            desc=f"Processing {self.name}",
            unit="item",
        ):
            # Create iteration context with original data and current item
            iteration_data = data.copy()
            iteration_data["_current_item"] = item
            iteration_data["_iteration_index"] = i

            # Process the iteration through the sub-pipeline
            if self.sub_pipeline.steps:
                result = self.sub_pipeline.process(iteration_data)
                results.append(result)
            else:
                # If no sub-steps, just append the current item
                results.append(iteration_data)

        # Store results in the output data
        data[self.results_key] = results
        return data
