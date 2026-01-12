from lib import SegmentTree
import sys


"""
TODO:
- 일단 SegmentTree부터 구현하기
- main 구현하기
"""


def main() -> None:
    # 구현하세요!
    input = sys.stdin.readline
    test_num = int(input())
    
    for _ in range(test_num):
        n, m = map(int, input().split())
        
        queries = list(map(int, input().split()))
        
        init_data = [0] * m + [1] * n
        st = SegmentTree(data=init_data, op=lambda a, b: a + b, e=0)
        position = [0] * (n + 1)
        for i in range(1, n + 1):
            position[i] = m + (i - 1)
        
        current_top = m -1
        result = []
        
        for movie_idx in queries:
            current_location = position[movie_idx]
            answer = st.query(0, current_location - 1)
            result.append(str(answer))
            
            st.update(current_location, 0)
            st.update(current_top, 1)
            
            position[movie_idx] = current_top
            current_top -= 1
        
        print(" ".join(result))
    


if __name__ == "__main__":
    main()