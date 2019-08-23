import os
curpath= os.getcwd()
filename=curpath + "\\" +"input.txt"

class Node:

    def __init__(self, data):

        self.left = None
        self.right = None
        self.data = data

    def insert(self, data):

        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data
    def move(self,u,v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v is not None:
            v.parent = u.parent

    def delete(self,node):
        if node.left is None:
            self.transplant(node,node.right)
        elif node.right is None:
            self.transplant(node,node.left)
        else:
            y = self.treeMinimum(node.right)
            if y.parent is not node:
                self.transplant(y,y.right)
                y.right = node.right
                y.right.parent = y
            self.transplant(node,y)
            y.left = node.left
            y.left.parent = y              
    def Print(self):
        if self.left:
            self.left.PrintTree()
        print( self.data),
        if self.right:
            self.right.PrintTree()
             
                            
                    
               # if (command=="MOVE"):
                   # root = move(lines.rsplit(" ")[1],lines.rsplit(" ")[1],lines.rsplit(" ")[2])        
                        

def performoperation(command,word):  
    if (command=="ADD"):
        root.insert(word)
    elif(command=="CREATE"):
        root = Node(word)
    elif(command=="DELETE"):
        root = Delete(word) 
    elif(command=="LIST"):
        List(node) 


root=Node("tree")
root.insert("fruits")
root.insert("tree")
root.insert("grains")





        
        

        

        



