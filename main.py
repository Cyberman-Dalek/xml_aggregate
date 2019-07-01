#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xml.dom.minidom
import math
from functools import reduce

class node:
    def __init__(self,x,y,z,r):
        self.x=x
        self.y=y
        self.z=z
        self.r=r
    def dist(self,other):
        return math.sqrt((self.x-other.x)**2+(self.y-other.y)**2+(self.z-other.z)**2)
    def neighbor(self,other):
        dist=self.dist(other)
        if self==other:
            return False
        if dist<self.r+other.r:
            return True
        else:
            return False

def max_dist(data):
    max_distance=-1
    max_index1=-1
    max_index2=-1
    for i in range(len(data)-1):
        for j in range(i+1,len(data)):
            dist=data[i].dist(data[j])
            if dist>max_distance:
                max_distance=dist
                max_index1=i
                max_index2=j
    return max_distance,max_index1,max_index2

def build_graph(data):
    graph=[]
    for i in range(len(data)):
        row=[]
        for j in range(len(data)):
            if i==j:
                row.append(0)
                continue
            if data[i].neighbor(data[j]):
                row.append(1);
            else:
                row.append(float('inf'))
        graph.append(row)
    return graph

def dijkstra(graph,src,target):
    nodes=[i for i in range(len(data))]
    visited=[]
    visited.append(src)
    nodes.remove(src)
    dis={src:0}
    while nodes:
        min_nodes = 500
        min_index = -1
        for v in visited:
            for d in nodes:
                if graph[src][v]!=float('inf') and graph[v][d]!=float('inf'):
                    new_dist=graph[src][v]+graph[v][d]
                    if graph[src][d]>new_dist:
                        graph[src][d]=new_dist
                    if graph[src][d]<min_nodes:
                        min_nodes=graph[src][d]
                        min_index = d
        dis[min_index]=min_nodes
        visited.append(min_index)
        nodes.remove(min_index)
    return dis[target]

def str2float(s):
    def fn(x,y):
        return 10*x+y
    n = s.index('.')
    if s[0] != '-':
        s1 = list(map(int, [x for x in s[:n]]))
        s2 = list(map(int, [x for x in s[n + 1:]]))
        return reduce(fn, s1) + reduce(fn, s2) / 10 ** len(s2)
    else:
        s1 = list(map(int, [x for x in s[1:n]]))
        s2 = list(map(int, [x for x in s[n + 1:]]))
        return -1*(reduce(fn, s1) + reduce(fn, s2) / 10 ** len(s2))


def read_xml(address):
    DOMTree = xml.dom.minidom.parse(address)
    collection = DOMTree.documentElement
    particles = collection.getElementsByTagName("particle")
    data=[]
    for particle in particles:
        position = particle.getElementsByTagName("position")[0]
        strPosition = position.childNodes[0].data
        listPosition = strPosition.split(',')
        x = str2float(listPosition[0][1:-1])
        y = str2float(listPosition[1][1:-1])
        z = str2float(listPosition[2][1:-1])
        radius = particle.getElementsByTagName("radius")[0]
        strRadius = radius.childNodes[0].data
        r = str2float(strRadius[1:-1])
        data.append(node(x,y,z,r))
    return data

if __name__ == '__main__':
    addresses = ["T/geometry"+str(i)+".xml" for i in range(0,100)]
    sumDist = 0
    sumMinNodes = 0
    for address in addresses:
        data = read_xml(address)
        max_distance, max_index1, max_index2 = max_dist(data)
        graph = build_graph(data)
        min_nodes = dijkstra(graph, max_index1, max_index2)
        sumDist = sumDist +max_distance
        sumMinNodes = sumMinNodes + min_nodes
    averageDist = sumDist/len(addresses)
    averageMinNodes = sumMinNodes/len(addresses)
    results={'AB距离平均值':averageDist,'AB间点数平均值':averageMinNodes}
    f=open('结果.txt','w+')
    f.write(str(results))

