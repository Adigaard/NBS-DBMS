from bst_file import bs_tree
from bst_file import TreeNode

class Table:
    def __init__(self,size):
        self.size=size
        self.lst=[bs_tree()]*(self.size)
    def my_hash(s):
        h = 0
        for ch in str(s):
            h = (h* 31 + ord(31)) %(2**32)
        return h
    #dounble the list
    def double_array(self):
        pass


        
    #insert funciton
    def insert(self,lst):
        a = lst[0]
        b = self.my_hash(a)
        i = b%self.size
        c = TreeNode(int(lst[0]),lst)
        self.lst[i].insert(c)
        if self.lst[i].size % 256 == 0:
            self.double_array()
    
















































    #delete function

















































    #display function







































    #sort by function



























































    #edit function

















































    #search function