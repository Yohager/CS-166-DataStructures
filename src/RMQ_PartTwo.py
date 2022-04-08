import math 
import random 
import time 

class CartesianTree:
    def __init__(self,array):
        self.array = array
        self.length = len(array)
    
    def Process(self):
        stack = []
        res_seq = ''
        idx = 0
        while idx < self.length:
            if not stack:
                res_seq += '1'
                stack.append(self.array[idx])
                idx += 1
            else:
                if self.array[idx] >= stack[-1]:
                    stack.append(self.array[idx])
                    res_seq += '1'
                    idx += 1
                else:
                    stack.pop()
                    res_seq += '0'
        while stack:
            stack.pop()
            res_seq += '0'
        # print(len(res_seq))
        # return ''.join(res_seq)
        return res_seq

class SparseTable:
    def __init__(self,array) -> None:
        self.array = array 
        self.n = len(self.array)
        self.dp = None 

    def lowbit(self,x): # using low bit to find the maximum k for the range
        return x & (-x)
        
    def find_k(self,v):
        while v - self.lowbit(v) != 0:
            v -= self.lowbit(v)
        return v 
        
    def find_size(self,v):
        if v == 1:
            return 0 
        cnt = 0
        while v != 1:
            v >>= 1 
            cnt += 1
        return cnt 
    
    def Construction(self):
        size = self.find_size(self.find_k(self.length))
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
        # rang = end - start + 1
        # minv = find_size(find_k(rang))
        # return min(dp[start][minv],dp[end-2**minv][minv])

class HybridMethod:
    def __init__(self,array):
        self.array = array
        self.n = len(array)
        self.block_size = int((math.log(x=self.n,base=2))/4)

    
    def BlockPartition(self):
        pass


    

if __name__ == "__main__":
    array = [27,18,28,18,28,45,90,45,23,53,60,28,74,71,35]
    CT1 = CartesianTree(array)
    print(CT1.Process())