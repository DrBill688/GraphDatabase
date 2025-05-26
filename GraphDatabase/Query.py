# -*- coding: utf-8 -*-
"""
@author: William N. Roney, ScD
"""
from typing import Self
from enum import StrEnum
from . import forcetype


class CombineOperator(StrEnum):
    AND = 'AND'
    OR = 'OR'
class Operator(StrEnum):
    EQUALS = 'EQ'
    NOT_EQUALS = 'NE'
    GREATER_THAN = 'GT'
    LESS_THAN = 'LT'

class QueryFilter():
    def __init__(self, DG, combine_operator: str, model_type: str, operator: str, value: str):
        self.combineOp = CombineOperator(forcetype.string(combine_operator).upper())
        self.filterOp = Operator(forcetype.string(operator).upper())
        self.strModelType = forcetype.string(model_type)
        if self.strModelType not in DG.fieldList():
            raise ValueError(f'{self.strModelType} does not exist in the GraphDatabase.')
        self.strValue = forcetype.string(value)
        return
    def __str__(self):
        return f'{self.combineOp} {self.strModelType} {self.filterOp} {self.strValue}'

class Query():
    def __init__(self, DG):
        self.G = DG
        self.root = None
        self.labels=self.G.fieldList()
        self.filters=None
        return
    def __str__(self) -> str:
        return "Query result as a string"
    def perspective(self , p_node) -> Self:
        self.root = p_node
        return self
    def attributes(self, *args) -> Self:
        selected = set()
        for arg in args:
            if self.G.G.has_edge(self.G._MODEL_TYPE, arg):
                selected.add(arg)
            else:
                raise ValueError(f'{arg} is not defined in the GraphDatabase')
        self.labels = list(selected)
        return self
    def restrictions(self, args) -> Self:
        if args is None:
            self.filters = None
        else:
            for arg in args:
                print(arg)
                combine_operator = None
                model_type = None
                operator = None
                value = None
                if len(arg) == 3:
                    combine_operator = CombineOperator.OR
                    model_type = arg[0]
                    operator = arg[1]
                    value = arg[2]
                elif len(arg) == 4:
                    combine_operator = arg[0]
                    model_type = arg[1]
                    operator = arg[2]
                    value = arg[3]
                else:
                    raise ValueError('Query.restrictions takes a list of ([AND|OR],<attr>,<operator>,<value>) tuples')
                if self.filters is None:
                    self.filters = []
                self.filters.append(QueryFilter(self.G, combine_operator, model_type, operator, value))
        return self
    def result(self) -> dict:
        print(f'Perspective: {self.root}')
        print(f'Attributes: {self.labels}')
        print(f'Restrictions: {self.filters if self.filters is None else [str(m) for m in self.filters]}')
        return {}
    