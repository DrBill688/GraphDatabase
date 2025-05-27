# -*- coding: utf-8 -*-
"""
@author: William N. Roney, ScD
"""

import networkx as nx
from typing import Self
from . import Query, forcetype, GraphDataStore

class GraphDatabase:
    __DEFAULT_SRCREF = 'n/a'
    __DEFAULT_DELIMITER = '=>'
    _MODEL_TYPE = 'ModelType'
    def __init__(self, delim = None):
        self.RDBMS = GraphDataStore.GraphDataStore()
        self.G = nx.DiGraph()
        self.delimiter = self.__DEFAULT_DELIMITER
        if delim is not None:
            self.delimiter = forcetype.string(delim)
        return
    def __str__(self) -> str:
        return f'{self.G}\n{self.RDBMS}'
    def query(self) -> Query.Query:
        return Query.Query(self)
    def shortest_path(self, source: str, destination: str):
        strSource = forcetype.string(source)
        strDest = forcetype.string(destination)
        if nx.has_path(self.G, strSource, strDest):
            return nx.shortest_path(self.G, strSource, strDest)
        elif nx.has_path(self.G.reverse(), strSource, strDest):
            return nx.shortest_path(self.G.reverse(), strSource, strDest)
        else:
            raise ValueError(f'No path between {strSource} and {strDest}')
    def successors(self, model_type) -> list:
        strModelType = forcetype.string(model_type)
        return [m for m in self.G.successors(strModelType) if m.startswith(f'{strModelType}{self.delimiter}')]
    def predecessors(self, node_type, node_val) -> list:
        node = f'{node_type}{self.delimiter}{node_val}'
        return [(m.split(self.delimiter)[0], m.split(self.delimiter)[1]) for m in self.G.predecessors(node) if len(m.split(self.delimiter)) == 2]
    def fieldList(self) -> list:
        print(f'fieldList ->\tin memory:({len(list(self.G.successors(self._MODEL_TYPE)))}) {list(self.G.successors(self._MODEL_TYPE))}')
        print(f'\t\t\tin datastore:({len(self.RDBMS.listModelFields())}) {self.RDBMS.listModelFields()}')
        return list(self.G.successors(self._MODEL_TYPE))
    def findall(self, model_type: str) -> list:
        prefix = f'{model_type}{self.delimiter}'
        return [m.replace(prefix, '') for m in self.G.successors(model_type) if m.startswith(prefix)]
    def find(self, model_type: str, child_node_list: list) -> list:
        res = []
        searchlist = child_node_list
        prefix = f'{model_type}{self.delimiter}'
        if type(child_node_list) == str:
            searchlist = [child_node_list]
        for edge in nx.edge_dfs(self.G.reverse(), searchlist):
            if edge[1].startswith(prefix):
                res.append(edge[1].replace(prefix, ''))
        return res
    def addEdge(self, uNode: str, vNode: str, source_ref: str) -> Self:
        strUNode = forcetype.string(uNode)
        strVNode = forcetype.string(vNode)
        strSourceRef = None
        if source_ref is not None and source_ref != self.__DEFAULT_SRCREF:
            strSourceRef = forcetype.string(source_ref)
            self.addSourceRef(strSourceRef)
        edge_data = self.G.get_edge_data(strUNode, strVNode, {'srcRef':[]})
        sources = set(edge_data['srcRef'])
        sources.add(strSourceRef)
        edge_data['srcRef'] = list(sources)
        self.G.add_edge(strUNode, strVNode, **edge_data)
        return self
    def addSourceRef(self, source_name: str) -> str:
        strSourceName = forcetype.string(source_name)
        self.addEdge('DataSource', strSourceName, self.__DEFAULT_SRCREF)
        if source_name != self.__DEFAULT_SRCREF:
            self.RDBMS.addSource(strSourceName)
        return strSourceName
    def addModelRelationship(self, parent_type: str, child_type: str, srcRef: str) -> Self:
        strParentType = forcetype.string(parent_type)
        strChildType = forcetype.string(child_type)
        if srcRef is not None:
            self.addSourceRef(srcRef)
        self.addEdge(self._MODEL_TYPE, strParentType, srcRef)
        self.addEdge(self._MODEL_TYPE, strChildType, srcRef)
        self.addEdge(strParentType, strChildType, srcRef)
        self.RDBMS.addModel(strParentType, strChildType, srcRef)
        return self
    def addRelationship(self, parent_type: str, parent_value: str, child_type: str, child_value: str, source_ref: str = None) -> Self:
        strParentType = forcetype.string(parent_type)
        strParentValue = forcetype.string(parent_value)
        strChildType = forcetype.string(child_type)
        strChildValue= forcetype.string(child_value)
        strSourceRef = self.__DEFAULT_SRCREF
        if source_ref is not None:
            strSourceRef = self.addSourceRef(source_ref)
        uNode = f'{strParentType}{self.delimiter}{strParentValue}'
        vNode = f'{strChildType}{self.delimiter}{strChildValue}'
        self.addModelRelationship(strParentType, strChildType, strSourceRef)
        self.addEdge(strParentType, uNode, strSourceRef)
        self.addEdge(strChildType, vNode, strSourceRef)
        self.addEdge(uNode, vNode, strSourceRef)
        self.RDBMS.addEdge(strParentType, strParentValue, strChildType, strChildValue, strSourceRef)
        return self
    def traverse(self, start_type: str, start_value:str) -> list:
        return [(m[0].split(self.delimiter)[0], m[0].split(self.delimiter)[1], m[1].split(self.delimiter)[0], m[1].split(self.delimiter)[1]) for m in nx.edge_bfs(self.G, f'{start_type}{self.delimiter}{start_value}')]
    
