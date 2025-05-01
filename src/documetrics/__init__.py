# For package initialization, this file is required to make Python treat the directory as a package.
import os
from typing import List, Dict, Any

import pandas as pd


from documetrics.FileLoader import FileLoader
from documetrics.MetricsDisplay import MetricsDisplay
from documetrics.ScoreAggregator import ScoreAggregator
from documetrics.globals import debug