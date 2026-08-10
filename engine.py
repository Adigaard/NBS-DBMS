from bst_file import bs_tree
from bst_file import TreeNode

class Table:
    def __init__(self,size):
        self.size=size
        self.lst = [bs_tree() for _ in range(self.size)]
    def my_hash(self,s):
        h = 0
        for ch in str(s):
            h = (h* 31 + ord(ch)) %(2**32)
        return h
    #dounble the list
    def double_array(self):
        a=[]
        for i in range (self.size):
            a.append(self.lst[i].inorder())
            self.lst[i].clean()
        self.size=self.size*2
        self.lst=[bs_tree() for _ in range(self.size)]
        for i in a :
            for j in i :
                self.insert(j)

        return 
        


        
    #insert funciton
    def insert(self,lst):
        a = lst[0]
        b = self.my_hash(a)
        i = b%self.size
        c = TreeNode(int(lst[0]),lst)
        self.lst[i].insert(c)
        if (self.lst[i].size == 256):
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
        n = self.lst[i].search_fn(k)
        if n == "ERROR: NOT FOUND":
            print("RECORD DOESNOT EXIST")
            return False
        try:
            idx = int(idx)
        except (TypeError, ValueError):
            print("INVALID COLUMN INDEX")
            return False
        if idx < 0 or idx >= len(n):
            print("COLUMN DOESNOT EXIST")
            return False
        if idx != 0:
            n[idx] = new_val
            return True
        nk = int(new_val)
        if nk == k:
            return True
        j = self.my_hash(new_val) % self.size
        if self.lst[j].search_fn(nk) !="ERROR: NOT FOUND":
            print("NEW KEY ALREADY EXISTS")
            return False
        rec = n
        rec[0] = new_val
        self.delete(key)
        self.insert(rec)
        return True
















































    #search function
    def search(self,val):
        a=self.my_hash(val)
        i=a%self.size
        return self.lst[i].search_fn(val)