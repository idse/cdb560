#!/bin/bash
# Start marimo with live updates (Claude's edits show up in the notebook).
# Usage:  ./start-notebook.sh                   (opens the file browser)
#         ./start-notebook.sh path/to/notebook.py
# Works both on Great Lakes (prints a link to open) and on your own computer
# (opens the browser for you).

NODE=$(hostname -f 2>/dev/null || hostname)

if [[ "$NODE" == *.arc-ts.umich.edu ]]; then
    # ---- On a Great Lakes compute node ----

    # pick a free port, so students sharing a node don't collide
    PORT=$(python3 -c 'import socket; s=socket.socket(); s.bind(("", 0)); print(s.getsockname()[1]); s.close()')

    # a random access token, so other users on the node can't open your notebook
    TOKEN=$(python3 -c 'import secrets; print(secrets.token_urlsafe(16))')

    BASE="/node/${NODE}/${PORT}"

    echo ""
    echo "  Open this link in your browser (Cmd+click):"
    echo ""
    echo "  https://greatlakes.arc-ts.umich.edu${BASE}/?access_token=${TOKEN}"
    echo ""
    echo "  Leave this terminal open. Press Ctrl+C here to stop marimo."
    echo ""

    # Hide the startup banner and watch notice; keep errors visible.
    exec uv run marimo --quiet --log-level ERROR edit "$@" \
        --watch --headless \
        --host 0.0.0.0 --port "$PORT" \
        --base-url "$BASE" \
        --token-password "$TOKEN"
else
    # ---- On your own computer ----
    echo ""
    echo "  Starting marimo; it will open in your browser."
    echo "  Leave this terminal open. Press Ctrl+C here to stop marimo."
    echo ""

    exec uv run marimo --quiet --log-level ERROR edit "$@" --watch
fi
