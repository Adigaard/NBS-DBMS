#from collections import deque
class TreeNode:
    def __init__(self,val,lst,left=None,right=None):
        self.val = val
        self.lst = lst
        self.left = left
        self.right = right

class bs_tree:
    def __init__(self):
        self.root=None
        self.size=0
    #insert function
    def insert(self,key):
        if(self.root == None):
            self.root=key
            self.size+=1
            return
        t = self.root
        while t:
            if t.val > key.val:
                if t.left == None:
                    t.left = key
                    self.size+=1
                    return
                t = t.left
            elif t.val < key.val:
                if t.right == None:
                    t.right = key
                    self.size+=1
                    return
                t = t.right



    #delete function
    def delete_fn(self, key):
        if(self.root==None):return None

        temp=self.root
        if(self.root.val==key):
            l=self.root.left
            r=self.root.right
            if(r==None):
                self.root=l
                self.size-=1
                return
            else:
                while(r.left!= None):r=r.left
                r.left=l
                r=self.root.right
                self.root=r
                self.size-=1
                return
        while(temp!= None):
            if(temp.val<key):
                if(temp.right!=None and temp.right.val == key):
                    l=temp.right.left
                    if(temp.right.right!=None): 
                        r=temp.right.right
                        while(r.left != None):r=r.left
                        r.left=l
                        temp.right=temp.right.right
                    else:
                        temp.right=l
                    break
                else:
                    temp=temp.right
            else:
                if(temp.left!=None and temp.left.val == key):
                    l=temp.left.left
                    if(temp.left.right!=None):
                        r=temp.left.right
                        while(r.left!=None): r=r.left
                        r.left=l
                        temp.left=temp.left.right
                    else:
                        temp.left=l
                    break
                else:
                    temp=temp.left
        if(temp==None):
            print("ERROR: Type data not found")
            return
        else: 
            self.size-=1
            return


    #search function
    def search_fn(self,key):
        temp=self.root
        while temp!=None:
            if key>temp.val:
                temp=temp.right
            elif key<temp.val:
                temp=temp.left
            else:
                break
        if temp==None:
            return "ERROR: NOT FOUND"
        else:
            return temp.lst

    #find min funciton
    #def min_node_fn(self):
    #    if(self.root==None):return "DATA NOT FOUND"
    #    temp=self.root
    #    while(temp.left!=None):temp=temp.left
    #    return temp


    #find max function
    #def max_node_fn(self):
    #    if(self.root==None):return "DATA NOT FOUND"
    #    temp=self.root
    #    while(temp.right!=None):temp=temp.right
    #    return temp

    #clear function
    def clean(self):
        self.root=None
        self.size=0
    #get height function
    #def GetHeight(self):
    #    if self.root is None:
    #    q = deque()
    #   height = -1
    #    q.append(self.root)
    #    while q:
    #        level_size = len(q)
    #        height += 1
#
    #        for i in range(level_size):
    #            curr = q.popleft()
#
    #            if curr.left is not None:
    #                q.append(curr.left)
#
    #            if curr.right is not None:
    #                q.append(curr.right)
#
    #    return height

  # inorder function
    def inorder(self):
        ans = []
        curr = self.root

        while curr is not None:
            if curr.left is None:
                ans.append(curr.lst)
                curr = curr.right
            else:
                temp = curr.left

                while temp.right is not None and temp.right is not curr:
                    temp = temp.right

                if temp.right is None:
                    temp.right = curr
                    curr = curr.left
                else:
                    temp.right = None
                    ans.append(curr.lst)
                    curr = curr.right

        return ans
