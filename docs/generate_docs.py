#!/usr/bin/env python3
"""
Script to regenerate API documentation automatically from docstrings.

This script should be run whenever the codebase changes.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(f"Error output: {e.stderr}")
        return None


def run_command_with_env(cmd, cwd=None, env=None):
    """Run a command with custom environment variables and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, env=env, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(f"Error output: {e.stderr}")
        return None


def generate_api_docs():
    """Generate API documentation from docstrings."""
    docs_dir = Path(__file__).parent
    project_root = docs_dir.parent

    print("🔄 Regenerating API documentation...")

    # Remove existing API docs
    api_dir = docs_dir / "api"
    if api_dir.exists():
        print("  📂 Removing existing API docs...")
        import shutil

        shutil.rmtree(api_dir)

    # Generate new API docs
    print("  📝 Generating new API docs...")
    cmd = (
        f"python -m sphinx.ext.apidoc -o api -H 'API Ref.' {project_root}/ai_graph --force --separate"
        " --templatedir ./_templates/apidoc -d 6 -M --remove-old -T"
    )
    result = run_command(cmd, cwd=docs_dir)

    if result is None:
        print("  ❌ Failed to generate API docs")
        return False

    # Fix module paths to include ai_graph prefix
    print("  🔧 Fixing module paths...")
    fix_module_paths(api_dir)

    print("  ✅ API documentation regenerated successfully!")
    return True


def fix_module_paths(api_dir):
    """Fix module paths in generated RST files to include ai_graph prefix."""
    replacements = [
        (".. automodule:: pipeline", ".. automodule:: ai_graph.pipeline"),
        (".. automodule:: step", ".. automodule:: ai_graph.step"),
        (".. automodule:: pipeline.base", ".. automodule:: ai_graph.pipeline.base"),
        (".. automodule:: step.base", ".. automodule:: ai_graph.step.base"),
        (".. automodule:: step.foreach", ".. automodule:: ai_graph.step.foreach"),
        (".. automodule:: step.video", ".. automodule:: ai_graph.step.video"),
        (".. automodule:: step.video.basic", ".. automodule:: ai_graph.step.video.basic"),
    ]

    for rst_file in api_dir.glob("*.rst"):
        content = rst_file.read_text()
        for old, new in replacements:
            content = content.replace(old, new)
        rst_file.write_text(content)


def build_docs():
    """Build the documentation."""
    docs_dir = Path(__file__).parent

    print("🏗️  Building documentation...")
    cmd = "python -m sphinx -b html . _build/html"
    result = run_command(cmd, cwd=docs_dir)

    if result is None:
        print("  ❌ Failed to build documentation")
        return False

    print("  ✅ Documentation built successfully!")
    return True


def execute_notebooks():
    """Execute notebooks from examples directory and copy to docs/examples."""
    docs_dir = Path(__file__).parent
    project_root = docs_dir.parent
    examples_src = project_root / "examples"
    examples_dst = docs_dir / "notebooks"

    print("📓 Processing example notebooks...")

    # Create examples directory if it doesn't exist
    examples_dst.mkdir(exist_ok=True)

    # Find all notebook files in examples directory
    notebook_files = list(examples_src.glob("*.ipynb"))

    if not notebook_files:
        print("  ℹ️  No notebooks found in examples directory")
        return True

    executed_notebooks = []

    for notebook_file in notebook_files:
        print(f"  📝 Processing {notebook_file.name}...")

        # Execute notebook using nbconvert with headless environment
        output_file = examples_dst / notebook_file.name

        # Set environment variables for headless execution
        env = os.environ.copy()
        env["DISPLAY"] = ":99"  # Virtual display
        env["QT_QPA_PLATFORM"] = "offscreen"  # Qt headless mode
        env["MPLBACKEND"] = "Agg"  # Matplotlib headless backend

        cmd = f"python -m jupyter nbconvert --to notebook --execute  {notebook_file}"

        # Copy notebook to destination first
        shutil.copy2(notebook_file, output_file)

        # Execute the copied notebook with headless environment
        result = run_command_with_env(cmd.replace(str(notebook_file), str(output_file)), cwd=docs_dir, env=env)

        if result is None:
            print(f"  ⚠️  Failed to execute {notebook_file.name}, copying original...")
            # Keep the original unexecuted version
        else:
            print(f"  ✅ Successfully executed {notebook_file.name}")

        executed_notebooks.append(
            {
                "filename": notebook_file.name,
                "title": extract_notebook_title(notebook_file),
                "path": f"examples/{notebook_file.name}",
            }
        )

    # Generate index file for examples
    generate_examples_index(examples_dst, executed_notebooks)

    print("  📋 Generated examples index file")
    print("  ✅ Notebook processing completed!")
    return True


def extract_notebook_title(notebook_path):
    """Extract title from notebook's first markdown cell."""
    try:
        with open(notebook_path, "r", encoding="utf-8") as f:
            notebook_content = json.load(f)

        # Look for first markdown cell with a title
        for cell in notebook_content.get("cells", []):
            if cell.get("cell_type") == "markdown" and cell.get("source"):
                source = "".join(cell["source"])
                # Look for markdown headers
                lines = source.split("\n")
                for line in lines:
                    line = line.strip()
                    if line.startswith("# "):
                        return line[2:].strip()

        # Fallback to filename without extension
        return notebook_path.stem.replace("_", " ").title()

    except Exception as e:
        print(f"  ⚠️  Could not extract title from {notebook_path.name}: {e}")
        return notebook_path.stem.replace("_", " ").title()


def generate_examples_index(examples_dir, notebooks):
    """Generate an index.rst file for the examples directory."""
    index_content = """Notebook Examples
========

This section contains example notebooks that demonstrate various features and use cases of the AI-Graph framework.

.. toctree::
   :maxdepth: 2
   :caption: Example Notebooks:

"""

    for notebook in notebooks:
        # Add notebook to toctree
        index_content += f"   {notebook['filename']}\n"

    index_content += """

Notebook Descriptions
--------------------

"""

    for notebook in notebooks:
        index_content += f"**{notebook['title']}**\n"
        index_content += f"   :doc:`{notebook['filename']}`\n\n"  # noqa

    # Write index file
    index_file = examples_dir / "index.rst"
    with open(index_file, "w", encoding="utf-8") as f:  # noqa
        f.write(index_content)


def main():
    """Run the documentation generation."""
    if len(sys.argv) > 1 and sys.argv[1] == "--build":
        # Just build, don't regenerate
        success = build_docs()
    else:
        # Regenerate API docs, execute notebooks, and build
        success = generate_api_docs()
        if success:
            success = execute_notebooks()
        if success:
            success = build_docs()

    if success:
        print("\n🎉 Documentation is ready!")
        print("   📖 Open _build/html/index.html to view the documentation")
        print("   📓 Examples are available in the documentation under Examples section")
    else:
        print("\n❌ Documentation generation failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
