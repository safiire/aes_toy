import galois
import numpy as np
from typing import Any

GF2  = galois.GF(2)
GF28 = galois.GF(2**8, irreducible_poly=galois.Poly.Int(0x11b))

Matrix = galois.FieldArray
Vector = galois.FieldArray
