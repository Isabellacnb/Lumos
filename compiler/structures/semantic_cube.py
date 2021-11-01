# -------------- semantic_cube.py --------------
# -- Rodrigo Bilbao -- Isabella Canales --
# 
# -- Lumos : Semantic Cube
# ----------------------------------------------


from enum import Enum

class Type(Enum):
    BOOL = 0
    INT = 1
    FLOAT = 2
    CHAR = 3
    STRING = 4
    VOID = 5

cube = {}

# Assign
cube['BOOL=BOOL'] = Type.BOOL
cube['INT=INT'] = Type.INT
cube['INT=CHAR'] = Type.INT
cube['INT=FLOAT'] = Type.INT
cube['FLOAT=FLOAT'] = Type.FLOAT
cube['FLOAT=INT'] = Type.FLOAT
cube['CHAR=INT'] = Type.CHAR
cube['CHAR=CHAR'] = Type.CHAR
cube['STRING=STRING'] = Type.STRING
cube['STRING=CHAR'] = Type.STRING

# Add
cube['INT+INT'] = Type.INT
cube['INT+CHAR'] = Type.INT
cube['INT+FLOAT'] = Type.FLOAT
cube['FLOAT+FLOAT'] = Type.FLOAT
cube['FLOAT+INT'] = Type.FLOAT
cube['CHAR+INT'] = Type.INT
cube['CHAR+CHAR'] = Type.STRING
cube['CHAR+STRING'] = Type.STRING
cube['STRING+CHAR'] = Type.STRING
cube['STRING+STRING'] = Type.STRING

# Subtract
cube['INT-INT'] = Type.INT
cube['INT-CHAR'] = Type.INT
cube['INT-FLOAT'] = Type.FLOAT
cube['FLOAT-FLOAT'] = Type.FLOAT
cube['FLOAT-INT'] = Type.FLOAT
cube['CHAR-INT'] = Type.INT
cube['CHAR-CHAR'] = Type.INT

# Divide
cube['INT/INT'] = Type.INT
cube['INT/CHAR'] = Type.INT
cube['INT/FLOAT'] = Type.FLOAT
cube['FLOAT/FLOAT'] = Type.FLOAT
cube['FLOAT/INT'] = Type.FLOAT
cube['CHAR/INT'] = Type.INT
cube['CHAR/CHAR'] = Type.INT

# Multiply
cube['INT*INT'] = Type.INT
cube['INT*CHAR'] = Type.INT
cube['INT*FLOAT'] = Type.FLOAT
cube['FLOAT*FLOAT'] = Type.FLOAT
cube['FLOAT*INT'] = Type.FLOAT
cube['CHAR*INT'] = Type.INT
cube['CHAR*CHAR'] = Type.INT

# Modular
cube['INT%INT'] = Type.INT
cube['INT%CHAR'] = Type.INT
cube['INT%FLOAT'] = Type.FLOAT
cube['FLOAT%FLOAT'] = Type.FLOAT
cube['FLOAT%INT'] = Type.FLOAT
cube['CHAR%INT'] = Type.INT
cube['CHAR%CHAR'] = Type.INT

# Equal
cube['BOOL==BOOL'] = Type.BOOL
cube['INT==INT'] = Type.BOOL
cube['INT==CHAR'] = Type.BOOL
cube['INT==FLOAT'] = Type.BOOL
cube['FLOAT==FLOAT'] = Type.BOOL
cube['FLOAT==INT'] = Type.BOOL
cube['CHAR==INT'] = Type.BOOL
cube['CHAR==CHAR'] = Type.BOOL
cube['STRING==CHAR'] = Type.BOOL
cube['CHAR==STRING'] = Type.BOOL
cube['STRING==STRING'] = Type.BOOL

# Unequal
cube['BOOL!=BOOL'] = Type.BOOL
cube['INT!=INT'] = Type.BOOL
cube['INT!=CHAR'] = Type.BOOL
cube['INT!=FLOAT'] = Type.BOOL
cube['FLOAT!=FLOAT'] = Type.BOOL
cube['FLOAT!=INT'] = Type.BOOL
cube['CHAR!=INT'] = Type.BOOL
cube['CHAR!=CHAR'] = Type.BOOL
cube['STRING!=CHAR'] = Type.BOOL
cube['CHAR!=STRING'] = Type.BOOL
cube['STRING!=STRING'] = Type.BOOL

# Less than
cube['INT<INT'] = Type.BOOL
cube['INT<CHAR'] = Type.BOOL
cube['INT<FLOAT'] = Type.BOOL
cube['FLOAT<FLOAT'] = Type.BOOL
cube['FLOAT<INT'] = Type.BOOL
cube['CHAR<INT'] = Type.BOOL
cube['CHAR<CHAR'] = Type.BOOL

# Greater than
cube['INT>INT'] = Type.BOOL
cube['INT>CHAR'] = Type.BOOL
cube['INT>FLOAT'] = Type.BOOL
cube['FLOAT>FLOAT'] = Type.BOOL
cube['FLOAT>INT'] = Type.BOOL
cube['CHAR>INT'] = Type.BOOL
cube['CHAR>CHAR'] = Type.BOOL

# Less than or equal
cube['INT<=INT'] = Type.BOOL
cube['INT<=CHAR'] = Type.BOOL
cube['INT<=FLOAT'] = Type.BOOL
cube['FLOAT<=FLOAT'] = Type.BOOL
cube['FLOAT<=INT'] = Type.BOOL
cube['CHAR<=INT'] = Type.BOOL
cube['CHAR<=CHAR'] = Type.BOOL

# Greater than or equal
cube['INT>=INT'] = Type.BOOL
cube['INT>=CHAR'] = Type.BOOL
cube['INT>=FLOAT'] = Type.BOOL
cube['FLOAT>=FLOAT'] = Type.BOOL
cube['FLOAT>=INT'] = Type.BOOL
cube['CHAR>=INT'] = Type.BOOL
cube['CHAR>=CHAR'] = Type.BOOL

# And
cube['BOOLandBOOL'] = Type.BOOL

# Or
cube['BOOLorBOOL'] = Type.BOOL

def getResultType(left, operator, right):
  l = left.name
  r = right.name
  key = l + operator + r
  if key in cube.keys():
    return cube[key]
  else:
    print("Invalid expression (type doesn't match). [", l, " and ", r, " don't match]")
    return None