#!/usr/bin/env python3
"""
Script to regenerate API documentation automatically from docstrings.

This script should be run whenever the codebase changes.
"""

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


def main():
    """Run the documentation generation."""
    if len(sys.argv) > 1 and sys.argv[1] == "--build":
        # Just build, don't regenerate
        success = build_docs()
    else:
        # Regenerate API docs and build
        success = generate_api_docs()
        if success:
            success = build_docs()

    if success:
        print("\n🎉 Documentation is ready!")
        print("   📖 Open _build/html/index.html to view the documentation")
    else:
        print("\n❌ Documentation generation failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
