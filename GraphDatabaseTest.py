# -*- coding: utf-8 -*-
"""
@author: William N. Roney, ScD
"""

import GraphDatabase as gdb

print('Start of test harness.')
DG = gdb.GraphDatabase()
print('Inserting data....')
srcRef = ('SourceName','20250525')
DG.addRelationship('Layer1', 'A', 'Layer1_description', 'This is A', srcRef)
DG.addRelationship('Layer1', 'A', 'Layer2', 1, srcRef)
DG.addRelationship('Layer1', 'A', 'Layer2', 1, ('SourceName','20250526'))
DG.addRelationship('Layer2', 1, 'Layer2_description', 'Widget1', ('SourceName','20250526'))
print('---------------------------')
print('Graph details:')
print(DG)
print(DG.G.edges)
print('---------------------------')
print('Query example:')
q = DG.query().perspective('Layer1') \
              .attributes('Layer1', 'Layer2_description') \
              .restrictions(None) \
              .result() 
print(q)
print('---------------------------')
print('Expecting an exception:')
q = DG.query().perspective('Layer1') \
              .restrictions([('Layer2', 'eq', 1), ('and', 'Layer3_missing', 'eq', '2025-10-02')]) \
              .result() 
print(q)
print('End of test harness.')
