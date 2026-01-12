from lib import Trie
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