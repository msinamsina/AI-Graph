Quick Start
===========

This guide will help you get started with AI-Graph in just a few minutes.

Your First Pipeline
-------------------

Let's create a simple pipeline that doubles numbers:

.. code-block:: python

   from ai_graph.pipeline import Pipeline
   from ai_graph.step import BaseStep

   class DoubleStep(BaseStep):
       """A step that doubles the input value."""

       def process(self, data):
           return data * 2

   # Create and run the pipeline
   pipeline = Pipeline()
   pipeline.add_step(DoubleStep())

   result = pipeline.run(input_data=5)
   print(f"Result: {result}")  # Output: Result: 10

Multiple Steps
--------------

You can chain multiple steps together:

.. code-block:: python

   from ai_graph.pipeline import Pipeline
   from ai_graph.step import BaseStep

   class AddStep(BaseStep):
       def __init__(self, value):
           self.value = value

       def process(self, data):
           return data + self.value

   class MultiplyStep(BaseStep):
       def __init__(self, value):
           self.value = value

       def process(self, data):
           return data * self.value

   # Create pipeline with multiple steps
   pipeline = Pipeline()
   pipeline.add_step(AddStep(10))      # Add 10
   pipeline.add_step(MultiplyStep(2))  # Multiply by 2

   result = pipeline.run(input_data=5)
   print(f"Result: {result}")  # Output: Result: 30 (5 + 10) * 2

Working with Collections
------------------------

Use ForEach steps to process collections:

.. code-block:: python

   from ai_graph.pipeline import Pipeline
   from ai_graph.step import BaseStep, ForEachStep

   class SquareStep(BaseStep):
       def process(self, data):
           return data ** 2

   # Create a sub-pipeline for each item
   sub_pipeline = Pipeline()
   sub_pipeline.add_step(SquareStep())

   # Create main pipeline with ForEach
   pipeline = Pipeline()
   pipeline.add_step(ForEachStep(sub_pipeline))

   numbers = [1, 2, 3, 4, 5]
   result = pipeline.run(input_data=numbers)
   print(f"Squared numbers: {result}")  # Output: [1, 4, 9, 16, 25]

Error Handling
--------------

AI-Graph provides built-in error handling:

.. code-block:: python

   from ai_graph.pipeline import Pipeline
   from ai_graph.step import BaseStep

   class DivideStep(BaseStep):
       def __init__(self, divisor):
           self.divisor = divisor

       def process(self, data):
           if self.divisor == 0:
               raise ValueError("Cannot divide by zero")
           return data / self.divisor

   pipeline = Pipeline()
   pipeline.add_step(DivideStep(0))

   try:
       result = pipeline.run(input_data=10)
   except ValueError as e:
       print(f"Error: {e}")  # Output: Error: Cannot divide by zero

Progress Tracking
-----------------

Enable progress tracking for long-running pipelines:

.. code-block:: python

   from ai_graph.pipeline import Pipeline
   from ai_graph.step import BaseStep, ForEachStep
   import time

   class SlowStep(BaseStep):
       def process(self, data):
           time.sleep(0.1)  # Simulate slow processing
           return data * 2

   # Create pipeline with progress tracking
   sub_pipeline = Pipeline()
   sub_pipeline.add_step(SlowStep())

   pipeline = Pipeline()
   pipeline.add_step(ForEachStep(sub_pipeline, show_progress=True))

   data = list(range(20))
   result = pipeline.run(input_data=data)
   # Shows progress bar: 100%|██████████| 20/20 [00:02<00:00,  9.95it/s]

Real-World Example
------------------

Here's a more practical example for text processing:

.. code-block:: python

   from ai_graph.pipeline import Pipeline
   from ai_graph.step import BaseStep, ForEachStep
   import re

   class CleanTextStep(BaseStep):
       def process(self, data):
           # Remove extra whitespace and convert to lowercase
           return re.sub(r'\s+', ' ', data.strip().lower())

   class CountWordsStep(BaseStep):
       def process(self, data):
           return len(data.split())

   class FilterLongTextsStep(BaseStep):
       def __init__(self, min_words=5):
           self.min_words = min_words

       def process(self, data):
           if data < self.min_words:
               return None  # Filter out short texts
           return data

   # Create text processing pipeline
   text_pipeline = Pipeline()
   text_pipeline.add_step(CleanTextStep())
   text_pipeline.add_step(CountWordsStep())
   text_pipeline.add_step(FilterLongTextsStep(min_words=3))

   # Process multiple texts
   main_pipeline = Pipeline()
   main_pipeline.add_step(ForEachStep(text_pipeline))

   texts = [
       "Hello World!",
       "This is a longer text with many words",
       "Short",
       "AI-Graph makes pipeline processing easy and efficient"
   ]

   results = main_pipeline.run(input_data=texts)
   # Filter out None values
   word_counts = [count for count in results if count is not None]
   print(f"Word counts: {word_counts}")  # Output: [3, 8, 7]

Next Steps
----------

Now that you've learned the basics, explore:

- :doc:`concepts` - Learn about the core concepts in detail
- :doc:`api/ai_graph` - Full API reference

Tips for Success
-----------------

1. **Keep steps small and focused** - Each step should do one thing well
2. **Use meaningful names** - Name your steps clearly to improve readability
3. **Handle errors gracefully** - Always consider what might go wrong
4. **Test your pipelines** - Write unit tests for your custom steps
5. **Use type hints** - AI-Graph supports full type checking with mypy
