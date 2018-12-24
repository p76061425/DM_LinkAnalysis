import numpy as np
import argparse
import math 
import sys

class Node:
    def __init__(self,name):
        self.name = name
        self.parentNodes  = {}
        self.childNodes = {}
        
class Graph:
    def __init__(self):
        self.nodes = {}
        self.name2idx = {}
        self.idx2name = []
    
    def load_data(self,graph_file):
        with open(graph_file, 'r') as f:
            lines = f.read().split()
        
        for line in lines:
            link = line.split(',')
            try:
                parentNode = self.nodes[int(link[0])]
            except:
                parentNode = Node(int(link[0]))
                self.nodes[parentNode.name] = parentNode
                self.idx2name.append(parentNode.name)
                self.name2idx[parentNode.name] = len(self.idx2name)-1
            try:
                childNode =  self.nodes[int(link[1])]
            except:
                childNode =  Node(int(link[1]))
                self.nodes[childNode.name] = childNode
                self.idx2name.append(childNode.name)
                self.name2idx[childNode.name] = len(self.idx2name)-1

            parentNode.childNodes[childNode.name] = childNode
            childNode.parentNodes[parentNode.name] = parentNode

def norm2(array):
    #return math.sqrt( np.sum(array**2) )
    return ( np.sum(array**2) )**0.5
    
def HubsAuthorities(graph,epsilon=1e-10):
    graph_size = len(graph.nodes)
    h_old = np.ones(graph_size)/graph_size ** 0.5
    a_old = np.ones(graph_size)/graph_size ** 0.5
    h_new = np.ones(graph_size)/graph_size ** 0.5
    a_new = np.ones(graph_size)/graph_size ** 0.5
    
    result_a = {}
    result_h = {}
   
    done = False
    while(not done):
        for curr_name,node in graph.nodes.items():
            curr_idx = graph.name2idx[curr_name]
            h_new[curr_idx] = 0
            a_new[curr_idx] = 0
            for parentName,parent in node.parentNodes.items():
                parent_idx = graph.name2idx[parentName]
                a_new[curr_idx] += h_old[parent_idx]
            for childName,child in node.childNodes.items():
                child_idx = graph.name2idx[childName]
                h_new[curr_idx] += a_old[child_idx]
            
        a_new /= norm2(a_new)
        h_new /= norm2(h_new)
        
        if( ( norm2(a_new-a_old) + norm2(h_new-h_old) )<epsilon ):
            done = True
           
        a_old = a_new.copy()
        h_old = h_new.copy()
            
    for idx,a in enumerate(a_new):
        result_a[graph.idx2name[idx]] = a
    for idx,h in enumerate(h_new):
        result_h[graph.idx2name[idx]] = h
    return result_a,result_h
    
def PageRank(graph, d=0.1, epsilon=1e-10):
    graph_size = len(graph.nodes)
    pr_old  = np.ones(graph_size) / graph_size
    pr_new  = np.ones(graph_size) / graph_size
    pr_result = {}
    done = False
    while(not done):
        for curr_name,node in graph.nodes.items():
            curr_idx = graph.name2idx[curr_name]
            pr_new[curr_idx] = 0
            
            for parentName,parent in node.parentNodes.items():
                parent_idx = graph.name2idx[parentName]
                pr_new[curr_idx] += pr_old[parent_idx] / len(parent.childNodes)
            pr_new[curr_idx] = d / graph_size + (1-d) * pr_new[curr_idx]

        pr_new /= norm2(pr_new)
        done = norm2(pr_old - pr_new) < epsilon
        pr_old = pr_new.copy()
        
        
    for idx,pr in enumerate(pr_new):
        pr_result[graph.idx2name[idx]] = pr
    return pr_result
            
"""            
class SimRank:
    def __init__(self,c,graph):
        self.c = c
        self.simRank_old = np.identity(len(graph.nodes))
        self.simRank_new = np.identity(len(graph.nodes))
        self.name2idx = graph.name2idx
        self.idx2name = graph.idx2name
        self.graph = graph
        self.nodes = graph.nodes
        
    def run(self):
        for a_name,a_node in self.nodes.items():
            for b_name,b_node in self.nodes.items():
                print(a_name,b_name)
                a_idx = self.name2idx[a_name]
                b_idx = self.name2idx[b_name]

                self.simRank_new[a_idx,b_idx] = self.sim(a_idx,b_idx)
                print(self.simRank_new[a_idx,b_idx])
        print(self.simRank_new)
        
        
    def sim(self,a_idx,b_idx):
        #print(self.idx2name[a_idx],self.idx2name[b_idx])
    
        a_parents = self.nodes[ self.idx2name[a_idx] ].parentNodes
        b_parents = self.nodes[ self.idx2name[b_idx] ].parentNodes
        if(len(a_parents)==0 or len(b_parents)==0):
            #print(0)
            return 0
        elif( self.idx2name[a_idx] == self.idx2name[b_idx] ):
            #print(1)
            return 1
        else:
            for in_a_name,in_a in a_parents.items():
                for in_b_name,in_b in b_parents.items():
                    in_a_idx = self.name2idx[in_a_name]
                    in_b_idx = self.name2idx[in_b_name]
                    
                    out = self.c/(len(a_parents)* len(b_parents)) *  self.sim(in_a_idx,in_b_idx)
                    return  out
"""        

class SimRank:
    def __init__(self,c,graph,epsilon=1e-10):
        self.c = c
        self.simRank_cal = np.identity(len(graph.nodes))
        self.name2idx = graph.name2idx
        self.idx2name = graph.idx2name
        self.graph = graph
        self.nodes = graph.nodes

    def sim(self,a_idx,b_idx):
        org = self.simRank_cal[a_idx,b_idx]
        
        a_parents = self.nodes[ self.idx2name[a_idx] ].parentNodes
        b_parents = self.nodes[ self.idx2name[b_idx] ].parentNodes
        
        if(len(a_parents)==0 or len(b_parents)==0):
            return 0,0        
        else:
            in_sim_sum = 0
            for in_a_name,in_a in a_parents.items():
                for in_b_name,in_b in b_parents.items():
                    in_a_idx = self.name2idx[in_a_name]
                    in_b_idx = self.name2idx[in_b_name]
                    in_sim_sum+=self.simRank_cal[in_a_idx,in_b_idx]
                    
            result = self.c/(len(a_parents)* len(b_parents)) * in_sim_sum
            err = (org - result)**2
            return result,err
        
    def run(self,):
        idx_size = len(self.name2idx)
        #print("idx_size",idx_size)
        done = False
        while(not done):
            err = 0
            for a_idx in range(idx_size):
                for b_idx in range(a_idx+1,idx_size):
                    #print(a_idx,b_idx)
                    self.simRank_cal[a_idx,b_idx],curr_err = self.sim(a_idx,b_idx)                    
                    self.simRank_cal[b_idx,a_idx] = self.simRank_cal[a_idx,b_idx]
                    err += curr_err
                    
            if err < epsilon: done = True
        
        return self.simRank_cal

def find_best(dict):
    best = sorted(dict.items(), key=lambda x:x[1], reverse=True)[0]
    best_name = best[0]    
    best_value = best[1]
    return best_name ,best_value 
    
def find_top5(dict):
    top_five = sorted(dict.items(), key=lambda x:x[1], reverse=True)[0:5]
    return top_five     
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f',
                        default="./hw3dataset/graph_1.txt",
                        dest='GRAPH_FILE',
                        help='graph file,(default="./hw3dataset/graph_1.txt")')
    parser.add_argument('-mode',
                        default="all",
                        dest='MODE',
                        help='ha=HubsAuthorities, pr=PageRank, sr=SimRank, all=all above, (default=all)')
    parser.add_argument('-d',
                        default=0.1,
                        type=float,
                        dest='D',
                        help='PageRank d, (default=0.1)')
    parser.add_argument('-c',
                        default=0.8,
                        type=float,
                        dest='C',
                        help='SimRank c, (default=0.8)')
    args = parser.parse_args()
    GRAPH_FILE = args.GRAPH_FILE
    MODE = args.MODE
    d = args.D
    c = args.C
    
    G = Graph()
    G.load_data(GRAPH_FILE)
     
    #check G
    #for key,node in G.nodes.items():
    #    print(key)
    #    print("node name",node.name)
    #    print("parentNodes:",node.parentNodes)
    #    print("childNodes:",node.childNodes)
    #print("name2idx",G.name2idx)    
    #print("idx2name",G.idx2name)
    
    if(MODE == "ha" or MODE == "all"):
        print()
        epsilon = 1e-10
        authorities,hubs = HubsAuthorities(G,epsilon)
        
        print("HubsAuthorities:")
        print("authorities:")
        best_authorities_name, best_authorities_value = find_best(authorities)
        print("best node:",best_authorities_name, "value:", best_authorities_value)
        #top5_authorities = find_top5(authorities)
        #print("top5:\n",top5_authorities)
        print(authorities)
        
        print("\nhub:")
        best_hub_name, best_hub_value = find_best(hubs)
        print("best node:",best_hub_name, "value:", best_hub_value )
        #top5_hubs = find_top5(hubs)
        #print("top5:\n",top5_hubs)
        print(hubs)

    if(MODE == "pr" or MODE == "all" ):
        print("-"*60)
        print("PageRank:")
        epsilon = 1e-10
        pageRank = PageRank(G,d,epsilon) 
        #top5_pageRank = find_top5(pageRank)
        #print("top5:\n",top5_pageRank)
        best_PageRank_name, best_PageRankvalue = find_best(pageRank)
        print("best node:",best_PageRank_name, "value:", best_PageRankvalue)
        print(pageRank)
        #for id in sorted(pageRank.keys()):
        #    print(id, pageRank[id])    
    
    if(MODE == "sr" or MODE == "all" ):
        print("-"*60)
        
        print("SimRank:")
        epsilon=1e-10
        simRank = SimRank(c,G,epsilon)
        simRank_result = simRank.run()    
        
        for a_idx,a_list in enumerate(simRank_result):
            print("="*30)
            print(G.idx2name[a_idx],"simRank:")
            for b_idx,sim in enumerate(a_list):
                if(sim!=0):
                    print(' ',G.idx2name[b_idx],":",sim)
        print("="*30)
        
        #max_simRank_value = np.max(simRank_result)
        #maxAidx = np.argmax(simRank_result, axis=0)[0]
        #maxBidx = np.argmax(simRank_result, axis=1)[0]
        #print(maxAidx,maxBidx, "value:",max_simRank_value )
        
        #check_idx1 = G.name2idx[7]
        #check_idx2 = G.name2idx[191]
        #print(simRank.simRank_cal[check_idx1,check_idx2])
        
    else:
        print("-mode must be ha=HubsAuthorities, pr=PageRank, sr=SimRank, all=all above,(default=all)")
            
        
    
