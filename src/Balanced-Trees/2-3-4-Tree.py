#2022.4.12 by yohager

import time 
import random 
import heapq 
import bisect 


class Node:
    def __init__(self):
        '''
        for each node in 2-3-4 tree
        there should be four slots for pointers 
        there should be three vals for keys 
        '''
        self.children = [None,None,None,None]
        self.vals = [] # here vals should be one min-heap
        self.parent = None 

    def __repr__(self) -> str:
        return f"vals: {self.vals}, children: {self.children}, parent: {self.parent}"
    
    def __str__(self) -> str:
        return str(self.val)

class TwoThreeFourTree:
    def __init__(self) -> None:
        self.root = Node()
    
    def _IsLeaf(self,node):
        for c in node.children:
            if c:
                return False 
        return True 
    
    def _CheckNode(self,v) -> Node:
        pass 
    
    def Insert(self,v,node) -> None:
        # v represents the value needed to be insert 
        # node represents the current node 
        cur = node 
        if len(cur.vals) == 0:
            # empty node 
            bisect.insort(cur.vals,v)
            return True 
        elif len(cur.vals) == 1:
            # 2-node 
            if self._IsLeaf(cur):
                bisect.insort(cur.vals,v)
                return True 
            else:
                if v < cur.vals[0]:
                    self.Insert(v,cur.children[0])
                else:
                    self.Insert(v,cur.children[1])
        elif len(cur.vals) == 2:
            if self._IsLeaf(cur):
                bisect.insort(cur.vals,v)
                return True 
            else:
                if v < cur.vals[0]:
                    self.Insert(v,cur.children[0])
                elif v < cur.vals[1]:
                    self.Insert(v,cur.children[1])
                else:
                    self.Insert(v,cur.children[2])
        elif len(cur.vals) == 3:
            '''
            this is the most difficult case 
            for 3-node 
            make division by the mid 

            '''

    def Search(self,v) -> Node:
        pass 

    def Delete(self,v) -> None:
        pass 
