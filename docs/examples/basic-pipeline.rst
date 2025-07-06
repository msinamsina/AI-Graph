Basic Pipeline Example
======================

This example demonstrates the fundamental concepts of AI-Graph by creating a simple data processing pipeline.

Problem Statement
-----------------

We need to process a list of user inputs by:

1. Cleaning and normalizing the text
2. Validating the data
3. Extracting specific information
4. Formatting the output

Solution Overview
-----------------

We'll create a pipeline with four steps:

1. **CleanStep**: Remove extra whitespace and normalize text
2. **ValidateStep**: Ensure data meets our requirements
3. **ExtractStep**: Extract useful information
4. **FormatStep**: Format the final output

Complete Example
----------------

.. code-block:: python

   from ai_graph.pipeline import Pipeline
   from ai_graph.step import BaseStep, ForEachStep
   from typing import Optional
   import re

   class CleanStep(BaseStep):
       """Clean and normalize input text."""

       def process(self, data: str) -> str:
           # Remove extra whitespace and convert to lowercase
           cleaned = re.sub(r'\s+', ' ', data.strip().lower())
           return cleaned

   class ValidateStep(BaseStep):
       """Validate that the input meets our requirements."""

       def process(self, data: str) -> Optional[str]:
           # Must be at least 3 characters and contain only letters/spaces
           if len(data) < 3:
               return None
           if not re.match(r'^[a-z\s]+$', data):
               return None
           return data

   class ExtractStep(BaseStep):
       """Extract the first and last words."""

       def process(self, data: str) -> dict:
           words = data.split()
           return {
               'first_word': words[0] if words else '',
               'last_word': words[-1] if words else '',
               'word_count': len(words),
               'original': data
           }

   class FormatStep(BaseStep):
       """Format the output as a readable string."""

       def process(self, data: dict) -> str:
           return (f"First: '{data['first_word']}', "
                   f"Last: '{data['last_word']}', "
                   f"Words: {data['word_count']}")

   # Create the pipeline
   def create_text_pipeline():
       pipeline = Pipeline()
       pipeline.add_step(CleanStep())
       pipeline.add_step(ValidateStep())
       pipeline.add_step(ExtractStep())
       pipeline.add_step(FormatStep())
       return pipeline

   # Test with a single input
   def test_single_input():
       pipeline = create_text_pipeline()

       test_input = "  Hello    Beautiful   World  "
       result = pipeline.run(input_data=test_input)
       print(f"Input: '{test_input}'")
       print(f"Result: {result}")
       # Output: First: 'hello', Last: 'world', Words: 3

   # Process multiple inputs
   def test_multiple_inputs():
       # Create a pipeline for individual items
       item_pipeline = create_text_pipeline()

       # Create a batch processing pipeline
       batch_pipeline = Pipeline()
       batch_pipeline.add_step(ForEachStep(item_pipeline))

       test_inputs = [
           "Hello World",
           "This is a longer sentence",
           "A",  # Too short, will be filtered
           "Python123",  # Invalid characters, will be filtered
           "AI Graph Framework",
           "   Extra   Spaces   Everywhere   "
       ]

       results = batch_pipeline.run(input_data=test_inputs)

       print("Batch Processing Results:")
       for i, (input_text, result) in enumerate(zip(test_inputs, results)):
           print(f"{i+1}. '{input_text}' -> {result}")

   if __name__ == "__main__":
       print("=== Single Input Test ===")
       test_single_input()

       print("\n=== Multiple Inputs Test ===")
       test_multiple_inputs()

Running the Example
-------------------

Save the code above to a file called ``basic_pipeline.py`` and run it:

.. code-block:: bash

   python basic_pipeline.py

Expected Output
---------------

.. code-block:: text

   === Single Input Test ===
   Input: '  Hello    Beautiful   World  '
   Result: First: 'hello', Last: 'world', Words: 3

   === Multiple Inputs Test ===
   Batch Processing Results:
   1. 'Hello World' -> First: 'hello', Last: 'world', Words: 2
   2. 'This is a longer sentence' -> First: 'this', Last: 'sentence', Words: 5
   3. 'A' -> None
   4. 'Python123' -> None
   5. 'AI Graph Framework' -> First: 'ai', Last: 'framework', Words: 3
   6. '   Extra   Spaces   Everywhere   ' -> First: 'extra', Last: 'everywhere', Words: 3

Key Concepts Demonstrated
-------------------------

1. **Step Composition**
   Each step has a single responsibility and can be combined with others.

2. **Data Validation**
   Steps can return ``None`` to filter out invalid data.

3. **Data Transformation**
   Steps can transform data from one format to another.

4. **Batch Processing**
   Use ``ForEachStep`` to apply the same pipeline to multiple inputs.

5. **Error Handling**
   Invalid inputs are gracefully handled and filtered out.

Variations and Extensions
-------------------------

Add Progress Tracking
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Add progress tracking for large datasets
   batch_pipeline = Pipeline()
   batch_pipeline.add_step(ForEachStep(
       item_pipeline,
       show_progress=True,
       progress_desc="Processing texts"
   ))

Add Error Handling
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   class SafeExtractStep(BaseStep):
       """Extract information with error handling."""

       def process(self, data: str) -> dict:
           try:
               words = data.split()
               return {
                   'first_word': words[0] if words else '',
                   'last_word': words[-1] if words else '',
                   'word_count': len(words),
                   'original': data
               }
           except Exception as e:
               # Log error and return safe default
               print(f"Error processing '{data}': {e}")
               return {
                   'first_word': '',
                   'last_word': '',
                   'word_count': 0,
                   'original': data,
                   'error': str(e)
               }

Add Conditional Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   class ConditionalFormatStep(BaseStep):
       """Format output differently based on word count."""

       def process(self, data: dict) -> str:
           if data['word_count'] == 1:
               return f"Single word: '{data['first_word']}'"
           elif data['word_count'] == 2:
               return f"Two words: '{data['first_word']}' and '{data['last_word']}'"
           else:
               return (f"Multiple words: starts with '{data['first_word']}', "
                       f"ends with '{data['last_word']}', "
                       f"total {data['word_count']} words")

Testing the Pipeline
--------------------

.. code-block:: python

   import pytest
   from your_module import CleanStep, ValidateStep, ExtractStep, FormatStep

   class TestPipelineSteps:
       def test_clean_step(self):
           step = CleanStep()
           result = step.process("  Hello    World  ")
           assert result == "hello world"

       def test_validate_step(self):
           step = ValidateStep()

           # Valid input
           assert step.process("hello world") == "hello world"

           # Invalid inputs
           assert step.process("hi") is None  # Too short
           assert step.process("hello123") is None  # Invalid chars

       def test_extract_step(self):
           step = ExtractStep()
           result = step.process("hello beautiful world")

           assert result['first_word'] == 'hello'
           assert result['last_word'] == 'world'
           assert result['word_count'] == 3

       def test_format_step(self):
           step = FormatStep()
           data = {
               'first_word': 'hello',
               'last_word': 'world',
               'word_count': 2
           }
           result = step.process(data)
           assert "First: 'hello'" in result
           assert "Last: 'world'" in result
           assert "Words: 2" in result

Next Steps
----------

Now that you understand the basics, try:

1. **Modify the steps** to handle different data types
2. **Add new steps** for additional processing
3. **Create your own pipeline** for a different use case
4. **Add error handling** and logging
5. **Experiment with different data flows**

Related Examples
----------------
