import os
import sys

from sphinx_pyproject import SphinxConfig

sys.path.append(
    os.path.abspath(f"{os.path.dirname(os.path.abspath(__file__))}/../../")
)

config = SphinxConfig("../../pyproject.toml", globalns=globals())
