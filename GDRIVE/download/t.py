# from its get path of file but different function give different performance

import os
print(os.path.join(os.path.dirname(__file__),"..","creds.json"))
print(os.path.dirname(__file__))
print(os.path.relpath(__file__))
print(os.path.realpath(__file__))
print(os.path.abspath(__file__))