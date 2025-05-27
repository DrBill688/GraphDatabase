# -*- coding: utf-8 -*-
"""
@author: William N. Roney, ScD
"""
from typing import Self
import pandas, json

class GraphDataStore:
    def __init__(self):
        self.sources = pandas.DataFrame(columns=['SourceRef'])
        self.model = pandas.DataFrame(columns=['ParentType', 'ChildType', 'SourceRef'])
        self.edges = pandas.DataFrame(columns=['ParentType', 'ParentValue', 'ChildType', 'ChildValue', 'SourceRef'])
        return
    def __str__(self) -> str:
        return f'Sources:\n{self.sources}\nModel:\n{self.model}\nEdges:\n{self.edges}'
    def addSource(self, source: str) -> Self:
        if len(self.sources[self.sources['SourceRef'] == source]) == 0:
            self.sources.loc[len(self.sources)] = [source]
        return self
    def addModel(self, pt, ct, sr)-> Self:
        matching_row = self.model[(self.model['ParentType'] == pt) & (self.model['ChildType'] == ct)] 
        if len(matching_row) == 0:
            self.model.loc[len(self.model)] = [pt, ct, sr]
        else:
            existing_sr = matching_row['SourceRef'].iloc[0]
            try:
                existing_sr = json.loads(existing_sr)
            except:
                existing_sr = [existing_sr]
            existing_sr.append(sr)
            self.model.loc[(self.model['ParentType'] == pt) & (self.model['ChildType'] == ct), 'SourceRef'] = json.dumps(existing_sr)
        return self
    def addEdge(self, pt, pv, ct, cv, sr)-> Self:
        matching_row = self.edges[(self.edges['ParentType'] == pt) & (self.edges['ParentValue'] == pv) & \
                                  (self.edges['ChildType'] == ct) & (self.edges['ChildValue'] == cv)] 
        if len(matching_row) == 0:
            self.edges.loc[len(self.edges)] = [pt, pv, ct, cv, sr]
        else:
            existing_sr = matching_row['SourceRef'].iloc[0]
            try:
                existing_sr = json.loads(existing_sr)
            except:
                existing_sr = [existing_sr]
            existing_sr.append(sr)
            self.edges.loc[(self.edges['ParentType'] == pt) & (self.edges['ParentValue'] == pv) & \
                           (self.edges['ChildType'] == ct) & (self.edges['ChildValue'] == cv), 'SourceRef'] = json.dumps(existing_sr)
        return self
    
