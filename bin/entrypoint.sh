#!/bin/bash
set -e

echo "Starting server..."
exec uv run -m app.main
