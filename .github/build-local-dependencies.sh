#!/bin/bash
#####################################
## Build Local Dependencies - /lib ##
#####################################
# Declare Variables
WORK_DIR=$(realpath "$0" | sed 's|\(.*\)/.*|\1|')
TEMP_DIR_PIP_INSTALL="temp_dir_pip_install_$$"
TEMP_DIR_PYDANTIC="temp_dir_pydanitc_$$"
REQUIREMENTS_FILE="requirements.txt"
COUNT=0
# Change in working directory
echo "=> Working Directory: $WORK_DIR"
cd $WORK_DIR
# Ensure that the temp-dirs are always deleted
trap 'echo "=> Cleanup temp-dirs..." ; rm -rf "$TEMP_DIR_PIP_INSTALL" ; rm -rf "$TEMP_DIR_PYDANTIC"' EXIT
# Check if <jq> is installed and exit if not
if ! command -v jq &> /dev/null; then
    echo "Error: <jq> is not installed. Please install it (e.g., 'sudo apt-get install jq')."
    exit 1
fi

# --- STEP 1: TEMP INSTALL PY-OLLAMA & EXTRACT DEPENDENT PYDANTIC-CORE VERSION ---
# Read the requirements to get the ollama version
OLLAMA_VERSION=$(grep '^ollama==' "../$REQUIREMENTS_FILE" | awk -F'==' '{print $2}')
if [ -z "$OLLAMA_VERSION" ]; then
    echo "Error: Could not find line for 'ollama==' in '$REQUIREMENTS_FILE'."
    exit 1
else
    echo "=> Ollama-Version: $OLLAMA_VERSION"
fi

echo "=> Create temp-dir: $TEMP_DIR_PIP_INSTALL"
mkdir -p "$TEMP_DIR_PIP_INSTALL"

echo "=> Install ollama==$OLLAMA_VERSION and its dependencies to $TEMP_DIR_PIP_INSTALL"
pip install "ollama==$OLLAMA_VERSION" \
    --target "$TEMP_DIR_PIP_INSTALL" \
    --quiet

if [ $? -ne 0 ]; then
    echo "Error: The pip installation failed."
    exit 1
fi

echo "=> Read the Pydantic-Core Version from the file system..."
DIST_INFO_DIR=$(ls "$TEMP_DIR_PIP_INSTALL" | grep 'pydantic_core.*\.dist-info' | head -n 1)

if [ -n "$DIST_INFO_DIR" ]; then
    # Extract the version (e.g. 2.33.2) from the name <pydantic_core-2.33.2.dist-info>
    PYDANTIC_CORE_VERSION=$(echo "$DIST_INFO_DIR" | sed -E 's/pydantic_core-(.*)\.dist-info/\1/')
    PYDANTIC_CORE_BASE_URL="https://pypi.org/pypi/pydantic-core/$PYDANTIC_CORE_VERSION/json"
    echo "Pydantic-Core Version: $PYDANTIC_CORE_VERSION"
else
    echo "Error: Could not find Pydantic-Core in the installation directory."
    exit 1
fi

# --- STEP 2: SCRAPE AND DOWNLOAD PYDANTIC-CORE WHEELS AND INSTALL LOCAL DEPENDENCIES ---
# Extract py-ver specific wheels automatically (Windows/x64 only)
#  e.g. "https://files.pythonhosted.org/packages/4f/53/a31aaa220ac133f05e4e3622f65ad9b02e6cbd89723d8d035f5effac8701/pydantic_core-2.33.0-cp39-cp39-win_amd64.whl"
PYDANTIC_CORE_FILE_URLS=($(curl -sL "$PYDANTIC_CORE_BASE_URL" | \
                           jq -r '.urls[].url' | \
                           grep -E "cp(39|310|311|312|313|314|315)-cp\1-win_amd64\.whl" | \
                           sort -u))

# Update/Clean PIP and install local dependencies
echo "=> Update PIP"
PEP668_FILE=$(python3 -c "import sysconfig; print(sysconfig.get_path('stdlib'))" 2>/dev/null)/EXTERNALLY-MANAGED
if [ -f "$PEP668_FILE" ] && command -v apt &>/dev/null; then
    echo "=> PEP 668 Schutz aktiv: Upgrade via sudo apt..."
    sudo apt-get update && sudo apt-get install --only-upgrade python3-pip -y
    PIP_FLAGS="--break-system-packages"
else
    echo "=> Upgrade via python3..."
    python3 -m pip install --upgrade pip
    PIP_FLAGS=""
fi
echo "=> Purge PIP cache for clean platform change"
pip cache purge
echo "=> Cleanup local dependencies (/lib)"
rm -r ../lib/*
echo "=> Install requirements with windows platform dependency"
pip install -r ../requirements.txt \
    --platform win_amd64 \
    --target ../lib \
    --only-binary=:all: \
    $PIP_FLAGS

# Pydantic Binary Library Handler
echo "=> Create and Change tmp dir: $TEMP_DIR_PYDANTIC"
mkdir -p $TEMP_DIR_PYDANTIC ; cd $TEMP_DIR_PYDANTIC

echo "=> Iterate over array, download wheels, extract and move *.pyd binaries"
for LINK in "${PYDANTIC_CORE_FILE_URLS[@]}"; do
    echo "$(($COUNT+1)). $LINK"
    wget "$LINK"
    FILE_NAME=$(basename "$LINK")
    unzip "$FILE_NAME"
    cp -n ./pydantic_core/_pydantic_core.*.pyd ../../lib/pydantic_core/
    rm -rf ./*
done

echo "=> Change to work dir and run into cleanup trap"
cd $WORK_DIR
