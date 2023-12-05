
class Pennant:
    
    def __init__(self, value=None)-> None:
        self.root = None if value == None else Node(item=value)

    def Pmerge(self,y):
        if self.root == None:
            return y
        else:
            self.root.right = y.root.left
            y.root.left = self.root
        
        return y

    def Pmerge_FA(self, x, y):
        if x == None and y == None and self.root == None:
            return None
        elif x==None and y==None:
            return self
        elif self.root==None and x==None:
            return y
        elif self.root==None and y==None:
            return x
        elif x==None:
            y=y.Pmerge(self)
            return None
        elif self.root==None:
            y=y.Pmerge(x)
            return None
        elif y==None:
            y=self.Pmerge(x)
            return None
        else:
            y=y.Pmerge(x)
            return self
        
        return None

    def Psplit(self):
        if self.root != None and self.root.left != None:
            y = Pennant()
            y.root= self.root.left
            self.root.left = y.root.right
            y.root.right=None
            return y
        return None

    def remove_all(self,node):
        if node.left!= None:
            self.remove_all(node.left)
        if node.right!=None:
            self.remove_all(node.right)
        del node

class Bag:
    def __init__(self, bag=None) -> None:
        self.forest_size = 20
        self.forest = self.forest_size*[None] if bag ==None else [f for f in bag.forest]

    
    def insert(self,item):
        i=0
        x = Pennant(item)

        while self.forest[i] != None:
            x = self.forest[i].Pmerge(x)
            self.forest[i]=None
            i+=1
        
        self.forest[i] = x

    
    def empty(self):

        for i in range(self.forest_size):
            if self.forest[i] != None:
                return False
        return True
    
    def merge(self,bag):
        carry = Pennant()
        size=self.forest_size
        for i in range(size):
            if self.forest[i] != None:
                self.forest[i] = self.forest[i].Pmerge_FA(bag.forest[i], carry)
            elif bag.forest[i] != None:
                self.forest[i] = bag.forest[i].Pmerge_FA(self.forest[i], carry)
            elif carry != None:
                self.forest[i] = carry
                carry = None
            else:
                self.forest[i]= None

    def split(self):
        new_bag = Bag()
        y = self.forest[0]
        self.forest[0]=None

        for i in range(1,self.forest_size):
            if self.forest[i] != None: 
                new_bag.forest[i-1] = self.forest[i].Psplit()
                self.forest[i-1] = self.forest[i]
                self.forest[i] = None
                    
    
        if y != None:
            self.insert(y.root.item)
            y.remove_all(y.root)
            del y
            y = None        
        
        return new_bag

    def clear(self):    
        for i in range(self.forest_size):
            self.forest[i] = None

    def size(self):
        sum = 0
        for i in range(self.forest_size):
            if self.forest[i] != None:
                sum += 2**i
        
        return sum


    def print(self):

        sum = 0
        print("***********TREES CONTAINING ITEMS:*************\n");
        for i in range(self.forest_size):
            sum = 0
            if self.forest[i] != None:
                self.recursive_print_sum(self.forest[i].root, sum)
                print(f'forest[{i}] has tree of size 2^{i} ={sum} \n')
            
        print("\n\n***********PRINTING CONTENTS:*************\n")
        
        for i in range(self.forest_size):
            if self.forest[i] != None:
                print(f'forest[{i}] contains: \n')
                self.recursive_print(self.forest[i].root);
            else:
                print(f'forest[{i}] = NULL\n')
        
        print("\n***********FINISHED*************\n\n")



    def recursive_print(self,node):

        if node.left != None:
            self.recursive_print(node.left);
        print(f'{node.item}')
        if node.right != None:
            self.recursive_print(node.right)


    def recursive_print_sum(self,node,sum):        
        sum+=1
        if sum == 1:
            if node.left != None:
                self.recursive_print_sum(node.left, sum)
        
        elif node.left != None:
            self.recursive_print_sum(node.left, sum)
        if node.right != None:
            self.recursive_print_sum(node.right, sum)

    
    def remove_all(self):
        
        for i in range(self.forest_size):
            self.forest[i].remove_all(self.forest[i].root)
            del self.forest[i]
            self.forest[i] = None
    

    def write_array(self):        
        size = self.size()
        array = size*[0]
        count = 0
        for i in range(self.forest_size):
            if(self.forest[i] != None):
                array,count = self.recursive_write_array(array, self.forest[i].root, count)
        return array

    
    def recursive_write_array(self,array, node, count):
        if node.left != None:
            array,count=self.recursive_write_array(array, node.left, count)
        array[count] = node.item
        count+=1

        if node.right != None:
            array,count = self.recursive_write_array(array, node.right, count)
            
        return array,count


class Bag_reducer(Bag):
    def __init__(self):
        self.imp_ = Bag()
        super().__init__()  

    def get_forest_size(self):  
        return self.imp_.forest_size;
  
    def get_forest(self,i):  
        return self.imp_.forest[i]
  
    def set_forest(self,i, tree):  
        self.imp_.forest[i] = tree
  
    def insert(self,item):
        self.imp_.insert(item)
  
    def merge(self,br):        
        self.imp_.merge(br.imp_)
  
    def split(self):  
        return self.imp_.split()
  
    def empty(self):
        return self.imp_.empty()
  
    def clear(self):  
        return self.imp_.clear()
  
    def get_reference(self):
        return self.imp_
  
    def size(self):
        return self.imp_.size()
  
    def write_array(self):
        return self.imp_.write_array()

class Node:
    def __init__(self,left = None, right= None, item=0)-> None:
        self.left = left
        self.right = right
        self.item = item
    



class Graph:
    def __init__(self,nv=None,ne=None,nbr=None,firstnbr=None) -> None:
        self.nv=nv
        self.ne=ne
        self.nbr=nbr
        self.firstnbr=firstnbr

