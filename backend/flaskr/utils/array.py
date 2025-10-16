import math
import random
from typing import List


def randElement[T](arr: List[T]) -> T:
    i = random.randrange(0, len(arr))
    return arr[i]