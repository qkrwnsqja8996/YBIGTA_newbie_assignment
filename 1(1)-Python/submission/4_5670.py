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
from typing import List, Optional # 추가

"""
TODO:
- 일단 Trie부터 구현하기
- count 구현하기
- main 구현하기
"""

def count(trie: Trie, query_seq: List[int]) -> int: # str을 List[int]로 변경
    """
    trie - 이름 그대로 trie
    query_seq - 단어 ("hello", "goodbye", "structures" 등)
    returns: query_seq의 단어를 입력하기 위해 버튼을 눌러야 하는 횟수
    """
    pointer: int = 0
    cnt: int = 0

    for element in query_seq:
        if len(trie[pointer].children) > 1 or trie[pointer].is_end:
            cnt += 1

        new_index: Optional[int] = None 
        for child_idx in trie[pointer].children:
            if trie[child_idx].body == element:
                new_index = child_idx
                break

        if new_index is not None: 
            pointer = new_index

    return cnt + int(len(trie[0].children) == 1)

def main() -> None:
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
                
            n = int(line.strip())
            
            trie: Trie[int] = Trie() 
            words: List[List[int]] = [] 
            
            for _ in range(n):
                word_str = sys.stdin.readline().strip()
                word_ords = [ord(c) for c in word_str]
                trie.push(word_ords)
                words.append(word_ords)
                
            total_press = 0
            for word_ords in words:
                total_press += count(trie, word_ords)
                
            print(f"{total_press / n:.2f}")
            
        except (ValueError, EOFError):
            break

if __name__ == "__main__":
    main()