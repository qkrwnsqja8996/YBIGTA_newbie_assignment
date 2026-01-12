from __future__ import annotations
from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Callable


"""
TODO:
- SegmentTree 구현하기
"""


T = TypeVar("T")
U = TypeVar("U")

@dataclass
class SegmentTree(Generic[T, U]):
    # 구현하세요!
    data: list[T]
    
    n: int = field(init=False)
    
    tree: list[U] = field(init=False)
    op : Callable[[U, U], U]
    e: U
    
    def __post_init__(self):
        self.n = len(self.data)
        self.tree = [self.e] * (self.n * 4)
        self._build(1, 0, self.n - 1)
    
    def _build(self, index: int, start: int, end: int) -> U:
        if start == end:
            self.tree[index] = self.data[start] # type: ignore
            return self.tree[index]
            
        mid = (start + end) // 2
        
        left_child = self._build(index * 2, start, mid)
        right_child = self._build(index * 2 + 1, mid + 1, end)
        
        self.tree[index] = self.op(left_child, right_child)
        
        return self.tree[index]
    
    def update(self, idx: int, value: T) -> None:
        self.data[idx] = value
        self._update(1, 0, self.n - 1, idx, value)
        
    def _update(self, index: int, start: int, end: int, target_idx: int, value: T) -> U:
        if target_idx < start or target_idx > end:
            return self.tree[index]
        
        if start == end:
            self.tree[index] = value # type: ignore
            return self.tree[index]
        
        mid = (start + end) // 2
        
        left_child = self._update(index * 2, start, mid, target_idx, value)
        right_child = self._update(index * 2 + 1, mid + 1, end, target_idx, value)
        
        self.tree[index] = self.op(left_child, right_child)
        return self.tree[index]
    
    def query(self, left: int, right: int) -> U:
        return self._query(1, 0, self.n - 1, left, right)
    
    def _query(self, index: int, start: int, end: int, q_start: int, q_end: int) -> U:
        if end < q_start or start > q_end:
            return self.e
        
        if q_start <= start and end <= q_end:
            return self.tree[index]
        
        mid = (start + end) // 2
        
        left_child = self._query(index * 2, start, mid, q_start, q_end)
        right_child = self._query(index * 2 + 1, mid + 1, end, q_start, q_end)
        
        return self.op(left_child, right_child)
    
    def find_kth(self, k: int) -> int:
        return self._find_kth(1, 0, self.n - 1, k)

    def _find_kth(self, index: int, start: int, end: int, k: int) -> int:
        if start == end:
            return start
            
        mid = (start + end) // 2
        left_count = self.tree[index * 2]
        
        if k <= left_count: # type: ignore
            return self._find_kth(index * 2, start, mid, k)
        else:
            return self._find_kth(index * 2 + 1, mid + 1, end, k - left_count) # type: ignore


import sys


"""
TODO:
- 일단 SegmentTree부터 구현하기
- main 구현하기
"""


class Pair(tuple[int, int]):
    """
    힌트: 2243, 3653에서 int에 대한 세그먼트 트리를 만들었다면 여기서는 Pair에 대한 세그먼트 트리를 만들 수 있을지도...?
    """
    def __new__(cls, a: int, b: int) -> 'Pair':
        return super().__new__(cls, (a, b))

    @staticmethod
    def default() -> 'Pair':
        """
        기본값
        이게 왜 필요할까...?
        """
        return Pair(0, 0)

    @staticmethod
    def f_conv(w: int) -> 'Pair':
        """
        원본 수열의 값을 대응되는 Pair 값으로 변환하는 연산
        이게 왜 필요할까...?
        """
        return Pair(w, 0)

    @staticmethod
    def f_merge(a: Pair, b: Pair) -> 'Pair':
        """
        두 Pair를 하나의 Pair로 합치는 연산
        이게 왜 필요할까...?
        """
        return Pair(*sorted([*a, *b], reverse=True)[:2])

    def sum(self) -> int:
        return self[0] + self[1]


def main() -> None:
    # 구현하세요!
    pass


if __name__ == "__main__":
    main()