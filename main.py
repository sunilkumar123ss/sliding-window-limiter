"""An exact request-count limiter over the interval (now - window, now]."""
import argparse
from collections import deque
import json
import math


