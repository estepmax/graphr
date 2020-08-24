import math,copy,random
 
class Node:
    def __init__(self,value,name=None):
        self.value = value 
        self.name = name
        self.visits = 0
        self.weight = 0
    
    def copy(self):
        return copy.deepcopy(self)

class GraphR(object):
    def __init__(self):
        self.graph = dict()  
        self.node_table = dict()
        
    def node_values(self):
        return [x.value for x in self.graph.keys()]

    def child_node_values(self,node):
        return [x.value for x in self.graph[node]]
    
    def insert_chained_edges(self,chain):
        for k in range(len(chain)-1):
            node0 = Node(chain[k]) if chain[k] not in self.node_table.keys() else self.node_table[chain[k]]
            node1 = Node(chain[k+1]) if chain[k+1] not in self.node_table.keys() else self.node_table[chain[k+1]]
            self.insert_edge(node0,node1)

    def insert_edge(self,start,end): 
        start.visits += 1     
        if end.value not in self.node_table.keys():
            self.node_table[end.value] = end
            self.graph[end] = []
        if start.value not in self.node_table.keys():
            self.node_table[start.value] = start
            child = end.copy()
            child.visits += 1
            self.graph[start] = [child]
        else:
            arg = None 
            children_values = self.child_node_values(start)
            if end.value in children_values:
                arg = children_values.index(end.value)
            if arg is not None:
                self.graph[start][arg].visits += 1
            else:
                child = end.copy()
                child.visits += 1
                self.graph[start].append(child) 
        
    def get_key_alias(self,node):
        parent = [x for x in self.graph.keys() if node.value == x.value]
        return parent[0]
    
    def node_weights(self):
        total = sum(list(map(lambda x: x.visits,self.graph.keys())))
        for node in self.graph.keys():
            node.weight = node.visits / total
    
    def child_node_weights(self):
        for node in self.graph.keys():
            total = sum(list(map(lambda x: x.visits,self.graph[node])))
            for child_node in self.graph[node]:
                child_node.weight = child_node.visits / total
    
    def dfs(self,start,queue=list()): 
        ## standard depth-first-search
        queue.append(start.value)
        for node in self.graph[start]:
            if node.value not in queue:
                parent = self.get_key_alias(node)
                self.dfs(parent,queue)
        return queue
    
    def max_depth(self,start,max_depth,queue=list()):  
        ## maximum depth-first-search 
        if len(queue) == max_depth: return queue
        queue.append(start.value)
        for node in self.graph[start]:
            if node.value not in queue:
                parent = self.get_key_alias(node)
                self.max_depth(parent,max_depth,queue)
        return queue
    
    def frequented(self,max):
        ## most frequented items (keys of the graph)
        weights = [(x,x.value,x.weight) for x in self.graph.keys()]
        weights.sort(reverse=True,key=lambda x:x[2])
        return weights[0:max]

