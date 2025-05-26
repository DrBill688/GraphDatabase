# -*- coding: utf-8 -*-
"""
@author: William N. Roney, ScD
"""

import networkx as nx
from typing import Self
from . import Query
from . import forcetype


class GraphDatabase:
    __DEFAULT_SRCREF = 'n/a'
    __DEFAULT_DELIMITER = '=>'
    _MODEL_TYPE = 'ModelType'
    def __init__(self, delim = None):
        self.G = nx.DiGraph()
        self.delimiter = self.__DEFAULT_DELIMITER
        if delim is not None:
            self.delimiter = forcetype.string(delim)
        return
    def __str__(self) -> str:
        return str(self.G)
    def query(self) -> Query.Query:
        return Query.Query(self)
    def fieldList(self) -> list:
        return list(self.G.successors('ModelType'))
    def addEdge(self, uNode: str, vNode: str, source_ref: str) -> Self:
        strUNode = forcetype.string(uNode)
        strVNode = forcetype.string(vNode)
        strSourceRef = forcetype.string(source_ref)
        edge_data = self.G.get_edge_data(strUNode, strVNode, {'srcRef':[]})
        sources = set(edge_data['srcRef'])
        sources.add(strSourceRef)
        edge_data['srcRef'] = list(sources)
        self.G.add_edge(strUNode, strVNode, **edge_data)
        return self
    def addSourceRef(self, source_name: str) -> str:
        strSourceName = forcetype.string(source_name)
        self.addEdge('DataSource', strSourceName, self.__DEFAULT_SRCREF)
        return strSourceName
    def addModelRelationship(self, parent_type: str, child_type: str, srcRef: str) -> Self:
        strParentType = forcetype.string(parent_type)
        strChildType = forcetype.string(child_type)
        self.addEdge(self._MODEL_TYPE, strParentType, srcRef)
        self.addEdge(self._MODEL_TYPE, strChildType, srcRef)
        self.addEdge(strParentType, strChildType, srcRef)
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
        self.addEdge(uNode, vNode, strSourceRef)
        return self
