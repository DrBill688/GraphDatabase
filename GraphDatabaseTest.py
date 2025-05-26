# -*- coding: utf-8 -*-
"""
@author: William N. Roney, ScD
"""

import json #for printing

import GraphDatabase as gdb

print('Start of test harness.')
DG = gdb.GraphDatabase()
print('Inserting data....')
srcRef = ('SourceName','20250525')
DG.addRelationship('Layer1', 'A', 'Layer1_description', 'This is A', srcRef)
DG.addRelationship('Layer1', 'A', 'Layer2', 1, srcRef)
DG.addRelationship('Layer1', 'B', 'Layer2', 1, ('SourceName','20250526'))
DG.addRelationship('Layer2', 1, 'Layer2_description', 'Widget1', ('SourceName','20250526'))
DG.addRelationship('Layer2', 1, 'Layer2_criteria', 'True', ('SourceName','20250526'))
DG.addRelationship('Layer2', 1, 'Layer3', 2)
DG.addRelationship('Layer3', 2, 'Layer3_description', 'Modelo')
print('---------------------------')
print('Graph details:')
print(DG)
print('---------------------------')
print('Query example 1: Layer2_description from Layer1')
q = DG.query().perspective('Layer1') \
              .attributes('Layer2_description') \
              .restrictions(None) \
              .result() 
print(json.dumps(q, indent=2))
print('Query example 2: Layer2_description from Layer1 if Layer2_criteria eq True')
q = DG.query().perspective('Layer1') \
              .attributes('Layer2_description') \
              .restrictions([('Layer2_criteria', 'eq', 'True')]) \
              .result() 
print(json.dumps(q, indent=2))
print('Query example 3:Layer1, Layer2_description from Layer2 if Layer2_criteria eq True')
q = DG.query().perspective('Layer2') \
              .attributes('Layer1', 'Layer2_description') \
              .restrictions([('Layer2_criteria', 'eq', 'True')]) \
              .result() 
print(json.dumps(q, indent=2))
print('Query example 4:Layer1, Layer2_description from Layer2 if Layer2_criteria ne True')
q = DG.query().perspective('Layer2') \
              .attributes('Layer1', 'Layer2_description') \
              .restrictions([('Layer2_criteria', 'ne', 'True')]) \
              .result() 
print(json.dumps(q, indent=2))
print('---------------------------')
print('Expecting an exception:')
try:
    q = DG.query().perspective('Layer1') \
                  .restrictions([('Layer2', 'eq', 1), ('and', 'Layer3_missing', 'eq', '2025-10-02')]) \
                      .result() 
    print('ERROR:  SHOULD HAVE THROWN AN EXCEPTION!  Layer3_missing is not in the graph.')
except ValueError as e:
    print(f'Correctly received: {e}')
print('End of test harness.')
