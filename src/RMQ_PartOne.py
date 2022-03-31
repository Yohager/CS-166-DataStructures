import math
import bisect 
import random 
import time 

class RMQ:
    def __init__(self,array) -> None:
        self.array = array 
        self.length = len(array)
    
    def NoPreprocessingRMQ(self,start,end):
        '''
        Solution 1
        <O(1),O(n)>
        '''
        if start > end:
            raise Exception("Invalid Query!")
        return min(self.array[start:end+1])
    
    def FullPreprocessing(self,start,end):
        '''
        Solution 2
        <O(n^2),O(1)>
        '''
        dp = [[float('inf')]*self.length for _ in range(self.length)]
        for i in range(self.length):
            dp[i][i] = self.array[i]
        for i in range(self.length-1,-1,-1):
            for j in range(i+1,self.length):
                dp[i][j] = min(dp[i][j-1],dp[i+1][j])
        # for x in dp:
        #     print(x)
        return dp[start][end]

    def BlockPartition(self,start,end):
        '''
        Solution 3 
        <O(n),O(n^{1/2})>
        '''
        size = int(math.sqrt(self.length)) # size of each block 
        minvs = []
        for i in range(0,self.length-1,size):
            minvs.append(min(self.array[i:min(i+size,self.length-1)]))
        block_cnt = len(minvs)
        start_block = start // size 
        start_left = start % size 
        end_block = end // size 
        end_left = end % size 
        if start_block == end_block:
            return min(self.array[start:end+1])
        else:
            mid_blocks = [minvs[x] for x in range(start_block+1,end_block)]
        # mid_blocks contains complete ranges 
            left_v = [self.array[v] for v in range(start_block*size+start_left,(start_block+1)*size)]
            right_v = [self.array[v] for v in range(end_block*size,end_block*size+end_left+1)]
            # print(left_v,right_v,mid_blocks)
            return min(left_v+mid_blocks+right_v)
    
    def SparseTable(self,start,end):
        '''
        Solution 4 
        <O(nlogn),O(1)>
        *For me, it is one important data structure
        '''
        def lowbit(x): # using low bit to find the maximum k for the range
            return x & (-x)
        
        def find_k(v):
            while v - lowbit(v) != 0:
                v -= lowbit(v)
            return v 
        
        def find_size(v):
            if v == 1:
                return 0 
            cnt = 0
            while v != 1:
                v >>= 1 
                cnt += 1
            return cnt 
        size = find_size(find_k(self.length))
        if 2**size < self.length:
            size += 1
        dp = [[float('inf')]*(size+1) for _ in range(self.length)]
        '''
        dp[i][2**k] = min(dp[i][2**(k-1)],dp[i+2**(k-1)][2**(k-1)])
        '''
        for i in range(self.length):
            dp[i][0] = self.array[i]
    
        '''
        for the dp, we should update the matrix by the cols 
        '''
        for k in range(1,size+1):
            for j in range(self.length):
                if (j+2**(k-1)) < self.length: 
                    dp[j][k] = min(dp[j][k-1],dp[j+2**(k-1)][k-1])
        # for x in dp:
        #     print(x)
        rang = end - start + 1
        minv = find_size(find_k(rang))
        return min(dp[start][minv],dp[end-2**minv][minv])


'''
no hybrid method has been implement in this file.
'''


if __name__ == "__main__":
    # array = [31,41,59,26,53,58,97,93]
    array = [random.randint(1,10000) for _ in range(10000)]
    RMQ1 = RMQ(array=array)
    start,end = random.randint(3,1000), random.randint(8000,9999)
    start_t = time.time()
    print(RMQ1.NoPreprocessingRMQ(start,end))
    t1 = time.time()
    print(RMQ1.FullPreprocessing(start,end))
    t2 = time.time()
    print(RMQ1.BlockPartition(start,end))
    t3 = time.time()
    print(RMQ1.SparseTable(start,end))
    t4 = time.time()
    print(t1-start_t,t2-t1,t3-t2,t4-t3)