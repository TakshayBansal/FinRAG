import sys
import os
from pathlib import Path

from finrag.utils import load_env_file, check_required_env_vars


if __name__ == "__main__":
    print(Path(__file__).parent.parent.parent.parent)
    load_env_file()
    check_required_env_vars()