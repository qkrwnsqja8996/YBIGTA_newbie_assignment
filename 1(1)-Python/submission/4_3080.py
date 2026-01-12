from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Iterable


"""
TODO:
- Trie.push 구현하기
- (필요할 경우) Trie에 추가 method 구현하기
"""


T = TypeVar("T")


@dataclass
class TrieNode(Generic[T]):
    body: Optional[T] = None
    children: list[int] = field(default_factory=lambda: [])
    is_end: bool = False


class Trie(list[TrieNode[T]]):
    def __init__(self) -> None:
        super().__init__()
        self.append(TrieNode(body=None))

    def push(self, seq: Iterable[T]) -> None:
        """
        seq: T의 열 (list[int]일 수도 있고 str일 수도 있고 등등...)

        action: trie에 seq을 저장하기
        """
        # 구현하세요!
        curr = 0
        for token in seq:
            found_index = -1
            t_ord = ord(token) if isinstance(token, str) else token
            target_children = self[curr].children
            
            if target_children and self[target_children[-1]].body == t_ord:
                found_index = target_children[-1]
            else:
                for index in target_children:
                    if self[index].body == t_ord:
                        found_index = index
                        break
                
            if found_index == -1:
                new_node = TrieNode(body=t_ord) # type: ignore
                self.append(new_node) # type: ignore
                found_index = len(self) - 1
                target_children.append(found_index)
            
            curr = found_index
        self[curr].is_end = True
            

    # 구현하세요!
    def calculate(self, node_idx: int) -> int:
        """
        Args:
            node_idx (int): 계산을 시작하는 현재 노드의 인덱스

        Returns:
            경우의 수를 1000000007로 나눈 나머지(int)
        """
        MOD = 1000000007
        if not hasattr(self, "fact"):
            self.fact = [1, 1]
            
        stack = [[node_idx, 0]]
        node_results = {}
        
        while stack:
            curr_idx, child_step = stack[-1]
            curr_node = self[curr_idx]
            children = curr_node.children
            
            if child_step == 0:
                group_count = len(children)
                if curr_idx != 0 and curr_node.is_end:
                    group_count += 1
                
                while len(self.fact) <= group_count:
                    self.fact.append(self.fact[-1] * len(self.fact) % MOD)
                
                node_results[curr_idx] = self.fact[group_count]
                
                if not children:
                    stack.pop()
                    continue
            
            if child_step < len(children):
                stack[-1][1] += 1
                stack.append([children[child_step], 0])
            else:
                final_val = node_results[curr_idx]
                for c_idx in children:
                    final_val = (final_val * node_results[c_idx]) % MOD
                    del node_results[c_idx]
                
                node_results[curr_idx] = final_val
                stack.pop()
                
        return node_results[node_idx]


import sys


"""
TODO:
- 일단 lib.py의 Trie Class부터 구현하기
- main 구현하기

힌트: 한 글자짜리 자료에도 그냥 str을 쓰기에는 메모리가 아깝다...
"""
sys.setrecursionlimit(100000)

def main() -> None:
    # 구현하세요!
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    
    words = sorted(input_data[1:])
    
    del input_data
    
    new_trie: Trie = Trie()
    for word in words:
        new_trie.push(word)
        
    del words
    
    print(new_trie.calculate(0))
        
if __name__ == "__main__":
    main()
    