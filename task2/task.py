from typing import Tuple
from task1.task import main as matrix_to_relations
import numpy as np

def main(s: str, e: str) -> Tuple[float, float]:
    rs = matrix_to_relations(s, e)
    size = len(rs[0]) - 1
    H = 0.0
    for r in rs:
        for row in r:
            n = sum(row)
            if n > 0:
                p = n / size
                H += -p * np.log2(p)
    H_norm = H / len(rs) / size
    return (round(H, 1), round(H_norm, 1))

if __name__ == '__main__':
    print(main("1,2\n1,3\n3,4\n3,5", "1"))
