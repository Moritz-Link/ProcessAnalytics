
import dill as pickle
import numpy as np
import torch
from torch_geometric.data import Data
import torch.nn.functional as F
import os


current_path = os.path.dirname(__file__) #'gnn_model.sav'
gnn =  pickle.load(open(os.path.join(current_path, "gnn_model.sav"), "rb"))
gnn.eval()

class Test():
    def calc(self,graph):
        prediciton = gnn(graph)
        print(f'prediciton {prediciton}')
        return prediciton
