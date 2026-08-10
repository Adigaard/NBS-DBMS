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
def delete(self,val):
    a=self.my_hash(val)
    i=a%(self.size)
    self.lst[i].delete_fn(val)
















































    #display function







































    #sort by function



























































    #edit function
    def edit(self, key, idx, new_val):
        k = int(key)
        i = self.my_hash(key) % self.size
        n = self.lst[i].search(k)
        if n is None:
            print("RECORD DOESNOT EXIST")
            return False
        try:
            idx = int(idx)
        except (TypeError, ValueError):
            print("INVALID COLUMN INDEX")
            return False
        if idx < 0 or idx >= len(n.val):
            print("COLUMN DOESNOT EXIST")
            return False
        if idx != 0:
            n.val[idx] = new_val
            return True
        nk = int(new_val)
        if nk == k:
            return True
        j = self.my_hash(new_val) % self.size
        if self.lst[j].search(nk) is not None:
            print("NEW KEY ALREADY EXISTS")
            return False
        rec = n.lst
        rec[0] = new_val
        self.delete(key)
        self.insert(rec)
        return True
















































    #search function