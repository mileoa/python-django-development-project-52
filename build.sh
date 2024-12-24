#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install uv
pip install uv

# Modify this line as needed for your package manager (pip, poetry, etc.)
uv sync

# Convert static asset files
uv run python manage.py collectstatic --no-input

# Apply any outstanding database migrations
uv run python manage.py migrate