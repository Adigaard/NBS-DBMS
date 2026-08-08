#insert function
def insert(head,key):
    
    t = head
    while t:
        if t.val > key.val:
            if t.left == None:
                t.left = key
                return
            t = t.left
        elif t.val < key.val:
            if t.right == None:
                t.right = key
                return
            t = t.right



#delete function
def delete_fn(head, key):
    if(head==None):return None
    temp=head
    if(head.val==key):
        l=head.left
        r=head.right
        if(r==None):return l
        else:
            while(r.left!= None):r=r.left
            r.left=l
            r=head.right
            del head
            return r
    while(temp!= None):
        if(temp.val<key):
            if(temp.right!=None and temp.right.val == key):
                l=temp.right.left
                if(temp.right.right!=None): 
                    r=temp.right.right
                    while(r.left != None):r=r.left
                    r.left=l
                    delnode=temp.right
                    temp.right=delnode.right
                    del delnode
                else:
                    a=temp.right
                    temp.right=l
                    del a
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
                    delnode=temp.left
                    temp.left=delnode.right
                    del delnode
                else:
                    a=temp.left
                    temp.left=l
                    del a
                break
            else:
                temp=temp.left
    if(temp==None):
        print("ERROR: Type data not found")
        return head
    else: return head
        


#search function
def search_fn(head,key):
    temp=head
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
def min_node_fn(head):
    if(head==None):return "DATA NOT FOUND"
    temp=head
    while(temp.left!=None):temp=temp.left
    return temp




#find max function
def max_node_fn(head):
    if(head==None):return "DATA NOT FOUND"
    temp=head
    while(temp.right!=None):temp=temp.right
    return temp





#get_size funciton
def get_size(head):
    if head==None:
        return 0
    return 1+get_size(head.left)+get_size(head.right)


#get height function
from collections import deque
def GetHeight(root):
    if root is None:
        return "ERROR: TREE NOT FOUND"
    q = deque()
    height = -1
    q.append(root)
    while q:
        level_size = len(q)
        height += 1

        for i in range(level_size):
            curr = q.popleft()

            if curr.left is not None:
                q.append(curr.left)

            if curr.right is not None:
                q.append(curr.right)

    return height


#clear function
#it resets a bst to none
def clean(head):
    head=None

