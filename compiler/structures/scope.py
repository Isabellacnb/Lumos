
from enum import Enum

# Scope enum
# ========================
class Scope(Enum):
  LOCAL = 0
  GLOBAL = 1
  TEMPORARY = 2
  CONSTANT = 3