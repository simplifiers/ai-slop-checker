import os
import sys

# Let test modules import "helpers" both with "python -m unittest" (from the repo root)
# and with "python -m unittest discover -s tests".
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
