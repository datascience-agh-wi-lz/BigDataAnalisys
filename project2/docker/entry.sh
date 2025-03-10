#!/bin/bash
# Debug mode for troubleshooting
[[ "$NXF_DEBUG_ENTRY" ]] && set -x

# Run the command directly
exec "$@"
