#!/bin/bash
#####################################
## Build Local Dependencies - /lib ##
#####################################
# Declare Variables
WORK_DIR=$(realpath "$0" | sed 's|\(.*\)/.*|\1|')
TMP_DIR="tmp_dir"
# CHANGE LINKS WHEN NEWER VERSION IS NEEDED (https://pypi.org/project/pydantic-core/2.33.0/#files)
PYDANTIC_CORE_LINKS=(
    "https://files.pythonhosted.org/packages/4f/53/a31aaa220ac133f05e4e3622f65ad9b02e6cbd89723d8d035f5effac8701/pydantic_core-2.33.0-cp39-cp39-win_amd64.whl"
    #"https://files.pythonhosted.org/packages/7d/67/cc789611c6035a0b71305a1ec6ba196256ced76eba8375f316f840a70456/pydantic_core-2.33.0-cp310-cp310-win_amd64.whl"
    "https://files.pythonhosted.org/packages/9a/26/d85a40edeca5d8830ffc33667d6fef329fd0f4bc0c5181b8b0e206cfe488/pydantic_core-2.33.0-cp311-cp311-win_amd64.whl"
    "https://files.pythonhosted.org/packages/be/3a/be78f28732f93128bd0e3944bdd4b3970b389a1fbd44907c97291c8dcdec/pydantic_core-2.33.0-cp312-cp312-win_amd64.whl"
    "https://files.pythonhosted.org/packages/13/8d/25ff96f1e89b19e0b70b3cd607c9ea7ca27e1dcb810a9cd4255ed6abf869/pydantic_core-2.33.0-cp313-cp313-win_amd64.whl"
)

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
for LINK in "${PYDANTIC_CORE_LINKS[@]}"; do
    wget "$LINK"
    FILE_NAME=$(basename "$LINK")
    unzip "$FILE_NAME"
    mv ./pydantic_core/_pydantic_core.*.pyd ../../lib/pydantic_core/
    rm -rf ./*
done

echo "=> Change to work dir and delete tmp dir"
cd $WORK_DIR ; rmdir $TMP_DIR
