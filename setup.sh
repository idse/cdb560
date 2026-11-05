#!/usr/bin/env bash
# One-time setup for CDB560. Run it once from the course folder:
#
#     ./setup.sh
#
# It installs "uv" (the tool that manages Python for this course) if needed,
# installs the Python packages, and checks that everything works.
# It is safe to run again: steps that are already done are skipped.
#
# Works on Great Lakes (VS Code via Open OnDemand) and on a Mac.

# Make sure we are running under bash (this line must stay plain POSIX sh syntax).
if [ -z "${BASH_VERSION:-}" ]; then
    echo "Please run this with:  bash setup.sh"
    exit 1
fi

# If the script was "sourced" (. setup.sh), 'exit' would close the terminal.
if [ "${BASH_SOURCE[0]}" != "$0" ]; then
    echo "Please run this with:  ./setup.sh   (not with 'source')"
    return 1
fi

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${TMPDIR:-/tmp}/cdb560-setup-$(id -un).log"
: > "$LOG_FILE"

# What we did, for the summary at the end.
SUMMARY=()
NEED_NEW_TERMINAL=0

say()  { echo "$*"; }
step() { echo ""; echo "== $* =="; }

# Print a plain-English error and stop.
#   usage: fail "what went wrong" "what to do"
fail() {
    echo ""
    echo "Something went wrong."
    echo ""
    echo "  What happened: $1"
    echo "  What to do:    $2"
    echo ""
    echo "  Technical details are saved in: $LOG_FILE"
    if [ -s "$LOG_FILE" ]; then
        echo "  (last lines of that file, to show your TA:)"
        tail -n 8 "$LOG_FILE" | sed 's/^/      /'
    fi
    echo ""
    exit 1
}

cd "$REPO_DIR" || fail "I could not open the course folder ($REPO_DIR)." \
    "Ask a TA for help."

if [ ! -f pyproject.toml ]; then
    fail "I can't find the file pyproject.toml next to setup.sh." \
        "Make sure you are running setup.sh from inside the course folder (cdb560). If that doesn't help, ask a TA."
fi

echo "CDB560 setup: this prepares your computer for the course."
echo "It can take a few minutes the first time. Please don't close this window."

# ---------------------------------------------------------------- 1. uv
step "Step 1 of 5: the 'uv' tool"

# uv installs itself in ~/.local/bin; make sure we look there even if the
# terminal's PATH doesn't (yet).
UV_WAS_ON_PATH=0
if command -v uv >/dev/null 2>&1; then
    UV_WAS_ON_PATH=1
else
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
fi

if command -v uv >/dev/null 2>&1; then
    say "uv is already installed ($(uv --version | cut -d" " -f2)). Skipping."
    SUMMARY+=("uv: already installed ($(uv --version | cut -d" " -f2))")
else
    say "uv is not installed yet. Installing it for your account (no admin rights needed)..."

    if ! command -v curl >/dev/null 2>&1; then
        fail "The program 'curl', which I need to download uv, is not available." \
            "Ask a TA for help."
    fi

    INSTALLER="$(mktemp "${TMPDIR:-/tmp}/uv-installer.XXXXXX")"
    if ! curl -LsSf https://astral.sh/uv/install.sh -o "$INSTALLER" >>"$LOG_FILE" 2>&1; then
        rm -f "$INSTALLER"
        fail "I could not download the uv installer. This usually means there is no internet connection (or the website is briefly down)." \
            "Check that you are connected to the internet, wait a minute and run ./setup.sh again. If it keeps failing, ask a TA."
    fi

    # UV_NO_MODIFY_PATH: we update your shell settings ourselves, below,
    # so that we know exactly what changes.
    if ! UV_NO_MODIFY_PATH=1 sh "$INSTALLER" >>"$LOG_FILE" 2>&1; then
        rm -f "$INSTALLER"
        fail "The uv installer stopped with an error." \
            "Run ./setup.sh again. If it fails a second time, ask a TA."
    fi
    rm -f "$INSTALLER"

    if ! command -v uv >/dev/null 2>&1; then
        fail "uv was installed, but I can't find it afterwards." \
            "Ask a TA for help."
    fi
    say "Installed $(uv --version | cut -d" " -f2)."
    SUMMARY+=("uv: installed ($(uv --version | cut -d" " -f2))")
fi

# Make uv available in future terminals: add ~/.local/bin to PATH in the
# shell settings file, unless it is already mentioned there.
UV_DIR="$(dirname "$(command -v uv)")"
if [ "$UV_DIR" = "$HOME/.local/bin" ]; then
    # single quotes on purpose: write a literal $HOME into the settings file
    # shellcheck disable=SC2016
    PATH_LINE='export PATH="$HOME/.local/bin:$PATH"  # added by CDB560 setup.sh'
else
    PATH_LINE="export PATH=\"$UV_DIR:\$PATH\"  # added by CDB560 setup.sh"
fi

add_path_to() {
    local rc_file="$1" must_exist="$2"
    if [ ! -f "$rc_file" ]; then
        [ "$must_exist" = "yes" ] && return 0
    fi
    if [ -f "$rc_file" ] && grep -q "$UV_DIR" "$rc_file" 2>/dev/null; then
        return 0
    fi
    # RHEL-style default .bashrc already adds ~/.local/bin; no need to repeat.
    if [ "$UV_DIR" = "$HOME/.local/bin" ] && [ -f "$rc_file" ] \
        && grep -q '\.local/bin' "$rc_file" 2>/dev/null; then
        return 0
    fi
    if { echo ""; echo "$PATH_LINE"; } >> "$rc_file" 2>>"$LOG_FILE"; then
        say "Added uv to $rc_file so future terminals can find it."
        SUMMARY+=("Shell settings: added uv to $rc_file")
        NEED_NEW_TERMINAL=1
    else
        say "Note: I could not edit $rc_file. uv works now, but you may need to run ./setup.sh again in a new terminal."
    fi
}

case "$(basename "${SHELL:-bash}")" in
    zsh)  add_path_to "$HOME/.zshrc" no;  add_path_to "$HOME/.bashrc" yes ;;
    *)    add_path_to "$HOME/.bashrc" no; add_path_to "$HOME/.zshrc" yes ;;
esac

if [ "$UV_WAS_ON_PATH" = 1 ]; then
    NEED_NEW_TERMINAL=0
fi

# ---------------------------------------------------------------- 2. packages
step "Step 2 of 5: Python and the course packages"
say "Installing (this is quick if it was done before)..."

if ! uv sync --compile-bytecode >>"$LOG_FILE" 2>&1; then
    fail "I could not install the Python packages. Common reasons: no internet connection, or your home folder is full." \
        "Check your internet connection and run ./setup.sh again. If it fails again, ask a TA and show them the lines below."
fi
say "Python packages are installed."
SUMMARY+=("Python packages: installed and up to date (folder .venv)")

# ---------------------------------------------------------------- 3. start-notebook.sh
step "Step 3 of 5: the notebook launcher"

if [ ! -f start-notebook.sh ]; then
    fail "I can't find the file start-notebook.sh in the course folder." \
        "Ask a TA for help."
fi
if [ -x start-notebook.sh ]; then
    say "start-notebook.sh is already ready to use. Skipping."
    SUMMARY+=("start-notebook.sh: already executable")
else
    if ! chmod +x start-notebook.sh 2>>"$LOG_FILE"; then
        fail "I could not make start-notebook.sh runnable." \
            "Ask a TA for help."
    fi
    say "Made start-notebook.sh ready to use."
    SUMMARY+=("start-notebook.sh: made executable")
fi

# ---------------------------------------------------------------- 4. VS Code extensions
step "Step 4 of 5: VS Code extensions"

# Great Lakes exposes code-server; desktop VS Code exposes code.
EDITOR_CLI=""
for candidate in code-server code; do
    if command -v "$candidate" >/dev/null 2>&1; then
        EDITOR_CLI="$candidate"
        break
    fi
done
EXTENSIONS_OK=1
if [ -n "$EDITOR_CLI" ] && INSTALLED_EXTENSIONS="$("$EDITOR_CLI" --list-extensions 2>>"$LOG_FILE")"; then
    for extension in ms-python.python anthropic.claude-code; do
        if printf '%s\n' "$INSTALLED_EXTENSIONS" | grep -Fxiq "$extension"; then
            say "$extension is already installed. Skipping."
        elif "$EDITOR_CLI" --install-extension "$extension" >>"$LOG_FILE" 2>&1; then
            if VERIFIED_EXTENSIONS="$("$EDITOR_CLI" --list-extensions 2>>"$LOG_FILE")" \
                && printf '%s\n' "$VERIFIED_EXTENSIONS" | grep -Fxiq "$extension"; then
                say "Installed $extension."
            else
                say "I could not confirm that $extension was installed."
                EXTENSIONS_OK=0
            fi
        else
            say "I could not install $extension automatically."
            EXTENSIONS_OK=0
        fi
    done
else
    say "Automatic extension installation is not available in this terminal."
    EXTENSIONS_OK=0
fi
if [ "$EXTENSIONS_OK" = 1 ]; then
    SUMMARY+=("VS Code extensions: Python and Claude Code are installed")
else
    say "Open View > Extensions in VS Code, search for Python and Claude Code,"
    say "and click Install for each. If that fails, ask a TA."
    say "Technical details for your TA are saved in: $LOG_FILE"
    SUMMARY+=("VS Code extensions: manual installation needed (View > Extensions)")
fi

# ---------------------------------------------------------------- 4. check
step "Step 5 of 5: checking that everything works"

# Read the package list from pyproject.toml and try to import each one,
# so this check always matches what the course needs.
CHECK_OUTPUT="$(uv run python - <<'PYEOF' 2>>"$LOG_FILE"
import importlib
import importlib.metadata
import re
import sys
import tomllib

# a few packages are imported under a different name than they are installed as
IMPORT_NAME = {"scikit-image": "skimage", "pillow": "PIL", "opencv-python": "cv2"}

with open("pyproject.toml", "rb") as f:
    dependencies = tomllib.load(f)["project"]["dependencies"]

all_ok = True
for requirement in dependencies:
    name = re.split(r"[<>=!~;\[ ]", requirement, maxsplit=1)[0]
    module = IMPORT_NAME.get(name.lower(), name.replace("-", "_"))
    try:
        importlib.import_module(module)
        version = importlib.metadata.version(name)
        print(f"  ok       {name} {version}")
    except Exception as error:
        all_ok = False
        print(f"  PROBLEM  {name}: {error}")
sys.exit(0 if all_ok else 1)
PYEOF
)"
CHECK_STATUS=$?
echo "$CHECK_OUTPUT"
echo "$CHECK_OUTPUT" >>"$LOG_FILE"

if [ "$CHECK_STATUS" -ne 0 ]; then
    fail "Some packages were installed but do not work (see 'PROBLEM' above)." \
        "Run ./setup.sh again. If the problem stays, ask a TA and show them this window."
fi
SUMMARY+=("Check: all course packages (including marimo) load correctly")

# ---------------------------------------------------------------- summary
echo ""
echo "=========================================="
if [ "$EXTENSIONS_OK" = 1 ]; then
    echo " Setup finished: all checks passed."
else
    echo " Python setup finished; extensions need attention."
fi
echo "=========================================="
for line in "${SUMMARY[@]}"; do
    echo "  - $line"
done
echo ""
echo "What to do next:"
if [ "$NEED_NEW_TERMINAL" = 1 ]; then
    echo "  1. Close this terminal and open a new one (in VS Code: click the"
    echo "     trash can icon, then Terminal > New Terminal), so that it knows about uv."
    echo "  2. In the new terminal, make sure you are in the course folder and run:"
else
    echo "  Start the notebook environment by running:"
fi
echo ""
echo "         ./start-notebook.sh"
echo ""
