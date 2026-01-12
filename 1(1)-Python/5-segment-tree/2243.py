from lib import SegmentTree
import sys


"""
TODO:
- 일단 SegmentTree부터 구현하기
- main 구현하기
"""


def main() -> None:
    # 구현하세요!
    readline = sys.stdin.readline
    MAX_TASTE = 1000000
    initial_data: list[int] = [0] * (MAX_TASTE + 1)
        
    st : SegmentTree = SegmentTree(initial_data, lambda a, b: a + b, 0)
    line = readline()
    if not line:
        return
    n : int = int(line.strip())   
     
    for _ in range(n):
        cmd = list(map(int, readline().split()))   
             
        if cmd[0] == 2:
            taste, count_diff = cmd[1], cmd[2]
            
            current_count = st.data[taste]
            st.update(taste, current_count + count_diff)
        
        elif cmd[0] == 1:
            rank = cmd[1]
            taste_idx = st.find_kth(rank)
            print(taste_idx)
            
            current_count = st.data[taste_idx]
            st.update(taste_idx, current_count - 1)

if __name__ == "__main__":
    main()