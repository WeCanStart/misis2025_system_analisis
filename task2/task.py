from typing import List, Tuple
from task1.task import main as matrix_to_relations
import numpy as np

# calculate graph entropy using main from task1.task
# and formula for particular node's and tuple's element entropy:
# calculate number of outgoing edges (n) and with s as number of nodes - 1 we have: H_ij = -n / s * log2(n / s)
# then result is sum of all H_ij (for all nodes and all tuple elements)

def main(csv_string: str) -> Tuple[int, int]:
    rs = matrix_to_relations(csv_string)
    H =  sum(sum(-sum(row) / (len(rs[0]) - 1) * (0 if sum(row) == 0 else np.log2(sum(row) / (len(rs[0]) - 1))) for row in r) for r in rs)
    return (H, H / len(rs) / (len(rs[0]) - 1))

if __name__ == '__main__':
    print(main('1,2\n1,3\n3,4\n3,5'))
