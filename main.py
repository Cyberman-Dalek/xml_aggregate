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
    try:
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
        if min_index == -1:#源点不能到达剩余点
            break
        dis[min_index]=min_nodes
        visited.append(min_index)
        nodes.remove(min_index)
    except BaseException:
       raise BaseException
    if target in dis.keys():
       return dis[target]
    else:#源点到不了目标点
        return float('inf')

def str2float(s):
    def fn(x,y):
        return 10*x+y
    #try:
    n = s.index('.')
    if 'E' in s:
        end = s.index('E')
        exp = s[end+1:]
        if exp[0] != '-':
          s1 = list(map(int, [x for x in exp]))
          expValue = reduce(fn, s1)
        else:
          s1 = list(map(int, [x for x in exp[1:]]))
          expValue = -1*reduce(fn, s1)
        if s[0] != '-':
          s1 = list(map(int, [x for x in s[:n]]))
          s2 = list(map(int, [x for x in s[n + 1: end]]))
          return (reduce(fn, s1) + reduce(fn, s2) / 10 ** len(s2))/10**expValue
        else:
          s1 = list(map(int, [x for x in s[1:n]]))
          s2 = list(map(int, [x for x in s[n + 1:end]]))
          return -1*(reduce(fn, s1) + reduce(fn, s2) / 10 ** len(s2))/10**expValue
    else:
        if s[0] != '-':
          s1 = list(map(int, [x for x in s[:n]]))
          s2 = list(map(int, [x for x in s[n + 1:]]))
          return reduce(fn, s1) + reduce(fn, s2) / 10 ** len(s2)
        else:
          s1 = list(map(int, [x for x in s[1:n]]))
          s2 = list(map(int, [x for x in s[n + 1:]]))
          return -1*(reduce(fn, s1) + reduce(fn, s2) / 10 ** len(s2))
    #except BaseException:
    #    print(s)
    #    raise BaseException

def read_xml(address):
    DOMTree = xml.dom.minidom.parse(address)
    collection = DOMTree.documentElement
    particles = collection.getElementsByTagName("particle")
    data=[]
    #try:
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
    #except BaseException:
    #    print(particles.index(particle))
    #    raise BaseException
    return data

if __name__ == '__main__':
    addresses = ["T/geometry"+str(i)+".xml" for i in range(0,100)]
    sumDist = 0
    sumMinNodes = 0
    spec = 0
    try:
     for address in addresses:
        data = read_xml(address)
        max_distance, max_index1, max_index2 = max_dist(data)
        graph = build_graph(data)
        min_nodes = dijkstra(graph, max_index1, max_index2)
        if min_nodes == float('inf'):#A不能到达B，忽略这种情况
            spec = spec +1
            continue
        sumDist = sumDist +max_distance
        sumMinNodes = sumMinNodes + min_nodes
    except BaseException:
        print(address)
    averageDist = sumDist/(len(addresses)-spec)
    averageMinNodes = sumMinNodes/(len(addresses)-spec)
    results={'AB距离平均值':averageDist,'AB间点数平均值':averageMinNodes}
    f=open('结果.txt','w+')
    f.write(str(results))

