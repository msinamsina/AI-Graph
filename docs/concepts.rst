Core Concepts
=============

Understanding the fundamental concepts of AI-Graph will help you build more effective processing pipelines.

The Chain of Responsibility Pattern
-----------------------------------

AI-Graph is built on the Chain of Responsibility design pattern, where:

- Each **Step** is a handler that processes data
- **Pipelines** chain these handlers together
- Data flows through the chain sequentially
- Each step can transform, filter, or enrich the data

.. code-block:: text

   # Data flows through the pipeline like this:
   Input → Step 1 → Step 2 → Step 3 → Output

Steps: The Building Blocks
--------------------------

Steps are the fundamental processing units in AI-Graph. Every step inherits from ``BaseStep`` and implements the ``process`` method.

Basic Step Structure
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ai_graph.step import BaseStep

   class MyStep(BaseStep):
       def process(self, data):
           # Your processing logic here
           return processed_data

Step Lifecycle
~~~~~~~~~~~~~~

Each step goes through this lifecycle:

1. **Initialization** - Create the step instance
2. **Processing** - Execute the ``process`` method
3. **Result** - Return the processed data

.. code-block:: python

   class LoggingStep(BaseStep):
       def __init__(self, message):
           self.message = message

       def process(self, data):
           print(f"{self.message}: {data}")
           return data  # Pass data through unchanged

Data Transformation Patterns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Steps can transform data in several ways:

**1. Transform**: Change the data structure or values

.. code-block:: python

   class UppercaseStep(BaseStep):
       def process(self, data):
           return data.upper()

**2. Filter**: Remove or conditionally pass data

.. code-block:: python

   class FilterPositiveStep(BaseStep):
       def process(self, data):
           return data if data > 0 else None

**3. Enrich**: Add additional information

.. code-block:: python

   class AddTimestampStep(BaseStep):
       def process(self, data):
           from datetime import datetime
           return {
               'data': data,
               'timestamp': datetime.now()
           }

**4. Aggregate**: Combine multiple pieces of data

.. code-block:: python

   class SumStep(BaseStep):
       def process(self, data):
           return sum(data) if isinstance(data, list) else data

Pipelines: Orchestrating the Flow
---------------------------------

Pipelines coordinate the execution of multiple steps in sequence.

Creating Pipelines
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ai_graph.pipeline import Pipeline

   # Create a pipeline
   pipeline = Pipeline()

   # Add steps
   pipeline.add_step(Step1())
   pipeline.add_step(Step2())
   pipeline.add_step(Step3())

   # Run the pipeline
   result = pipeline.run(input_data=data)

Pipeline Execution Model
~~~~~~~~~~~~~~~~~~~~~~~~

When you run a pipeline:

1. Data is passed to the first step
2. Each step processes the data from the previous step
3. The final step's output becomes the pipeline result
4. If any step returns ``None``, the pipeline stops

.. code-block:: python

   # Example execution flow
   data = "hello"

   # Step 1: Uppercase → "HELLO"
   # Step 2: Add prefix → "PREFIX: HELLO"
   # Step 3: Count chars → 13

   result = 13

Error Handling in Pipelines
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pipelines handle errors gracefully:

.. code-block:: python

   class RiskyStep(BaseStep):
       def process(self, data):
           if data < 0:
               raise ValueError("Negative values not allowed")
           return data * 2

   pipeline = Pipeline()
   pipeline.add_step(RiskyStep())

   try:
       result = pipeline.run(input_data=-5)
   except ValueError as e:
       print(f"Pipeline failed: {e}")

ForEach: Processing Collections
-------------------------------

The ``ForEachStep`` enables processing collections of data by applying a sub-pipeline to each item.

Basic ForEach Usage
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ai_graph.step import ForEachStep

   # Create a sub-pipeline
   item_pipeline = Pipeline()
   item_pipeline.add_step(DoubleStep())

   # Use ForEach to apply it to a collection
   main_pipeline = Pipeline()
   main_pipeline.add_step(ForEachStep(item_pipeline))

   numbers = [1, 2, 3, 4, 5]
   result = main_pipeline.run(input_data=numbers)
   # Result: [2, 4, 6, 8, 10]

ForEach with Fixed Iterations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also use ForEach for a fixed number of iterations:

.. code-block:: python

   from ai_graph.step import ForEachStep

   # Run the same pipeline 5 times
   pipeline = Pipeline()
   pipeline.add_step(ForEachStep(sub_pipeline, iterations=5))

   result = pipeline.run(input_data=initial_value)

Progress Tracking
~~~~~~~~~~~~~~~~~

Enable progress bars for long-running ForEach operations:

.. code-block:: python

   pipeline.add_step(ForEachStep(
       sub_pipeline,
       show_progress=True,
       progress_desc="Processing items"
   ))

Data Flow Patterns
------------------

Understanding how data flows through your pipeline is crucial for design.

Linear Flow
~~~~~~~~~~~

The simplest pattern where data flows sequentially:

.. code-block:: text

   Input → Clean → Validate → Transform → Output

Branching Flow
~~~~~~~~~~~~~~

Use conditional steps to create branching logic:

.. code-block:: python

   class ConditionalStep(BaseStep):
       def process(self, data):
           if condition(data):
               return process_path_a(data)
           else:
               return process_path_b(data)

Filtering Flow
~~~~~~~~~~~~~~

Remove unwanted data at various stages:

.. code-block:: text

   Input → Filter1 → Process → Filter2 → Output

Aggregation Flow
~~~~~~~~~~~~~~~~

Combine multiple data points:

.. code-block:: text

   Collection → ForEach(Process) → Aggregate → Output

Best Practices
--------------

1. **Single Responsibility**
   Each step should have one clear purpose.

2. **Immutable Data**
   Avoid modifying input data; return new data instead.

3. **Error Handling**
   Always consider what can go wrong and handle it gracefully.

4. **Type Safety**
   Use type hints to make your code more robust.

5. **Testing**
   Write unit tests for each step individually.

6. **Documentation**
   Document what each step does and its expected input/output.

Example: Complete Pipeline
--------------------------

Here's a complete example showing all concepts:

.. code-block:: python

   from ai_graph.pipeline import Pipeline
   from ai_graph.step import BaseStep, ForEachStep
   from typing import List, Optional

   class ValidateEmailStep(BaseStep):
       """Validates email format."""

       def process(self, email: str) -> Optional[str]:
           if '@' in email and '.' in email:
               return email
           return None  # Invalid emails are filtered out

   class NormalizeEmailStep(BaseStep):
       """Normalizes email to lowercase."""

       def process(self, email: str) -> str:
           return email.lower().strip()

   class ExtractDomainStep(BaseStep):
       """Extracts domain from email."""

       def process(self, email: str) -> str:
           return email.split('@')[1]

   # Create email processing pipeline
   email_pipeline = Pipeline()
   email_pipeline.add_step(ValidateEmailStep())
   email_pipeline.add_step(NormalizeEmailStep())
   email_pipeline.add_step(ExtractDomainStep())

   # Process multiple emails
   batch_pipeline = Pipeline()
   batch_pipeline.add_step(ForEachStep(email_pipeline, show_progress=True))

   emails = [
       "John.Doe@GMAIL.COM",
       "invalid-email",
       "alice@example.org",
       "bob@company.com"
   ]

   domains = batch_pipeline.run(input_data=emails)
   # Result: ['gmail.com', 'example.org', 'company.com']
   # (invalid email was filtered out)

This example demonstrates:
- Data validation and filtering
- Data transformation (normalization)
- Data extraction
- Batch processing with ForEach
- Progress tracking
- Type hints for better code quality
