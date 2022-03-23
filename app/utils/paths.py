import os
from pathlib import Path
import shutil

WORKING_DIR = os.path.dirname(__file__)
ROOT_DIR = Path(WORKING_DIR).parent.parent
MOCK_DATA_DIR = os.path.join(ROOT_DIR, "test")
TMP_DIR = os.path.join(ROOT_DIR, "tmp")
OUTPUTS_DIR = os.path.join(ROOT_DIR, "outputs")

# Ensure Tmp_dir exists and is empty
if os.path.exists(TMP_DIR):
    shutil.rmtree(TMP_DIR)

os.mkdir(TMP_DIR)


# Ensure static_dir exists and is empty

if os.path.exists(OUTPUTS_DIR):
    shutil.rmtree(OUTPUTS_DIR)

os.mkdir(OUTPUTS_DIR)
