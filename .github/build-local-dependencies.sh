#!/bin/bash
#####################################
## Build Local Dependencies - /lib ##
#####################################
# Declare Variables
WORK_DIR=$(realpath "$0" | sed 's|\(.*\)/.*|\1|')
TMP_DIR="tmp_dir"
COUNT=0
# Change the Pydantic-Core Version as needed
PYDANTIC_VERSION="2.33.1"
PYDANTIC_CORE_BASE_URL="https://pypi.org/project/pydantic-core/$PYDANTIC_VERSION/#files"
# Extract py-ver specific wheels automatically (Windows/x64 only)
#  e.g. "https://files.pythonhosted.org/packages/4f/53/a31aaa220ac133f05e4e3622f65ad9b02e6cbd89723d8d035f5effac8701/pydantic_core-2.33.0-cp39-cp39-win_amd64.whl"
PYDANTIC_CORE_FILE_URLS=($(curl -s "$PYDANTIC_CORE_BASE_URL" | \
                            grep -oE 'https://files\.pythonhosted\.org/packages/[^"]+' | \
                            grep -E "cp(39|310|311|312|313)-cp\1-win_amd64\.whl" | \
                            sort -u))

# Change in working directory
echo "=> Working Directory: $WORK_DIR"
cd $WORK_DIR

# Update/Clean PIP and install local dependencies
echo "=> Update PIP"
python3 -m pip install --upgrade pip
echo "=> Purge PIP cache for clean platform change"
pip cache purge
echo "=> Cleanup local dependencies (/lib)"
rm -r ../lib/*
echo "=> Install requirements with windows platform dependency"
pip install -r ../requirements.txt \
    --platform win_amd64 \
    --target ../lib \
    --only-binary=:all:

# Pydantic Binary Library Handler
echo "=> Create and Change tmp dir: $TMP_DIR"
mkdir -p $TMP_DIR ; cd $TMP_DIR

echo "=> Iterate over array, download wheels, extract and move *.pyd binaries"
for LINK in "${PYDANTIC_CORE_FILE_URLS[@]}"; do
    echo "$(($COUNT+1)). $LINK"
    wget "$LINK"
    FILE_NAME=$(basename "$LINK")
    unzip "$FILE_NAME"
    cp -n ./pydantic_core/_pydantic_core.*.pyd ../../lib/pydantic_core/
    rm -rf ./*
done

echo "=> Change to work dir and delete tmp dir"
cd $WORK_DIR ; rmdir $TMP_DIR
