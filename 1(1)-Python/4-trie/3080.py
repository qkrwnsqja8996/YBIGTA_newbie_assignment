from lib import Trie
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
    