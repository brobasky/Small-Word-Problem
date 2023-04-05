from collections import deque
from collections import defaultdict
import pandas as pd


def loadGraph(filename):
    #reading to df
    edgedf=pd.read_csv(filename,sep=' ',header=None,names=['p1','p2'])
    #list of nodes
    nodesraw=edgedf['p1'].to_list()+edgedf['p2'].to_list()
    nodes=[]
    for vertex in nodesraw:
        if vertex not in nodes:
            nodes.append(vertex)
    #loop thru nodes list, find each instance of node, adds corresponding nodes to dict value
    G={}
    for V in nodes:
        p1df=edgedf.loc[edgedf['p1']==V]
        connections1=p1df['p2'].to_list()
        p2df=edgedf.loc[edgedf['p2']==V]
        connections2=p2df['p1'].to_list()
        connections=connections1+connections2
        G[V]=connections
    return G

class MyQueue(deque):
    def empty(self):
        if len(self)>0:
            return False
        else:
            return True
    def enqueue(self,item):
        self.append(item)
    def dequeue(self):
        self.popleft()
    def front(self):
        return self[0]


#clean up your notes and ramblings but I think this is good otherwise
def BFS(G,s):
    nodes=list(G.keys())
    degreecount=MyQueue([])
    #the length of this after calling the function proves that all 4039 nodes are connected to some degree
    visitednodes={s}
    #visitednodes.append(s) bug moment
    q=MyQueue([])
    q.enqueue(s)
    #keeps track of nodes in the tier, starts with just s
    tier=[s]
    nexttier=[]
    while q.empty()==False:
        s2=q.front()
        if s2 in tier: #check if the node is in the current breadth
            for node in G[s2]:
                if node not in visitednodes:
                    visitednodes.add(node)
                    q.enqueue(node)
                    nexttier.append(node)
            q.dequeue()
        #when we reach a node that isn't in the current tier, the 'tier' list is replaced with the 'nexttier' list
        #after this, the 'nexttier' list is emptied
        else:
            degreecount.enqueue(len(tier))
            tier=nexttier
            nexttier=[]
    #getting rid of entry for zero degrees of separation
    degreecount.dequeue()
    return degreecount

#this takes a long time, but it works eventually
def distanceDistribution(G):
    '''
    -call bfs on each node, then add the results to corresponding entries in master_list
    -use a try except to append to the end if theres an index error
    '''
    count=0
    nodes=list(G.keys())
    master_list=[]
    for vertex in nodes:
        counts=BFS(G,vertex)
        for i in range(len(counts)):
            try:
                master_list[i]+=counts[i]
            except IndexError:
                master_list.append(counts[i])
        count+=1
        if count%40==0:
            print(f'~{count/40}% complete')


    percents_dict={}
    for i in range(len(master_list)):
        percents_dict[f'{i+1} degrees']=f'{(master_list[i]/sum(master_list))*100}%'

    return percents_dict



def main():
    #running the full distanceDistribution function
    #I included a screenshot of the terminal output in the folder since this takes a while to run
    graph=loadGraph('edges.txt')
    DD=distanceDistribution(graph)
    print(DD)

    '''
    #some testing code for the breadth first search

    degrees=BFS(graph,897)
    print(degrees)

    degrees=BFS(graph,40)
    print(degrees)

    degrees=BFS(graph,0)
    print(degrees)

    degrees=BFS(graph,2117)
    print(degrees)
    '''


if __name__ == '__main__':
    main()


'''
    I think that the small world phenomenon holds on this dataset.  Only about 1%
of people in the dataset are more than 6 degrees of separation apart, and no one
was more than 7 degrees apart.  The majority of people have 3-4 degrees of separation.
'''
