#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
#pip install -r requirements.txt
pip install uv
uv sync
# Convert static asset files
uv run python3 manage.py collectstatic --no-input

# Apply any outstanding database migrations
uv run python3 manage.py migrate

if [[ $CREATE_SUPERUSER ]];
then
  python world_champ_2022/manage.py createsuperuser --no-input
fi
