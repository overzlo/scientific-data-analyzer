# Ensure the repository root is on sys.path so that `import src` works in any environment
import sys
from pathlib import Path

# Resolve project root as the parent of the tests directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Prepend to sys.path if not already present
project_root_str = str(PROJECT_ROOT)
if project_root_str not in sys.path:
    sys.path.insert(0, project_root_str)
