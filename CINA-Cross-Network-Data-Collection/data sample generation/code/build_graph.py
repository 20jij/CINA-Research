import re
import requests
import json
import numpy as np
import networkx as nx
import pickle
import random
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
import torch
import time
from scipy.sparse import coo_matrix
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
import pickle

from prunning_methods import *

def before_year(year, hop):
    orig_features_file_git = 'static_features_' + str(year) + '.json'
    target_features_file_git = 'static_features_2008_' + str(year) + '.json'
    edges_file_git = 'gid_edges.txt'
    G_git, adj_matrix_git, static_array_git = json2graph(orig_features_file_git, target_features_file_git, edges_file_git, hop)
    return G_git, adj_matrix_git, static_array_git

print("Github graph start")

year = 2021
git_hop = 1
stack_hop = 2

data = {}
data['year'] =  str(year)

# orig_features_file_git = 'static_features_' + str(year) + '.json'
# target_features_file_git = 'static_features_2008_' + str(year) + '.json'
# edges_file_git = 'gid_edges.txt'
# G_git, adj_matrix_git, static_array_git= before_year(year, git_hop)
# data['git_nodes_hop_' + str(git_hop)] = len(G_git.nodes())
# data['git_edges_hop_' + str(git_hop)] = len(G_git.edges())

# with open('G_git_' + str(year) + '_hop' + str(git_hop) + '.pkl', 'wb') as fp:
#     pickle.dump(G_git, fp)
# with open('adj_matrix_git_'+ str(year) + '_hop' + str(git_hop) + '.pkl', 'wb') as fp:
#     pickle.dump(adj_matrix_git, fp)
# with open('static_array_git_' + str(year) + '_hop' + str(git_hop) + '.pkl', 'wb') as fp:
#     pickle.dump(static_array_git, fp)

with open(r"C:\Users\Jason Ji\Desktop\CINA\model\G_git_2021_hop1.pkl", "rb") as fp:
    G_git = pickle.load(fp)
with open(r"C:\Users\Jason Ji\Desktop\CINA\model\adj_matrix_git_2021_hop1.pkl", 'rb') as fp:
    adj_matrix_git = pickle.load(fp)
with open(r"C:\Users\Jason Ji\Desktop\CINA\model\static_array_git_2021_hop1.pkl", 'rb') as fp:
    static_array_git = pickle.load(fp)



print("Stackoverflow start")

# build the github nodes json file 
git_nodes = {}
for node in G_git.nodes():
    git_nodes[node] = 1
with open('git_nodes.json', 'w') as file:
    json.dump(git_nodes, file, indent=4)


G_stack, cross_edge = stackGraph('git_nodes.json', stack_hop)

with open('G_stack_' + str(year) + '_hop' + str(stack_hop) + '.pkl', 'wb') as fp:
    pickle.dump(G_stack, fp)

data['stack_nodes_hop_' + str(stack_hop)] = len(G_stack.nodes())
data['stack_edges_hop_' + str(stack_hop)] = len(G_stack.edges())
data['stack_cross_edges'] = cross_edge


print(data)

# features_file_git = '../data_preprocess/static_features_not_none.json'
# edges_file_git = '../data_preprocess/gid_edges.txt'
# G_git, adj_matrix_git, static_array_git = json2graph(features_file_git, edges_file_git)
# data_generation(G_git, adj_matrix_git, static_array_git, 100, percentage=10, diffusion='LT', dataset='../CINA_data/github/github')

# node_file_stack = '../data_preprocess/sid_all.txt'
# edge_file_stack = '../data_preprocess/all_sid_link_edges.txt'
# G_stack, adj_matrix_stack = text2graph(node_file_stack, edge_file_stack)
# with open('../CINA_data/gitHub/G_stack_pruned.pkl', 'rb') as fp:
#     G_stack = pickle.load(fp)
adj_matrix_stack = nx.to_numpy_array(G_stack, dtype='f')
# features_file_git = '../data_preprocess/static_features_not_none.json'
# edges_file_git = '../data_preprocess/gid_edges.txt'
# G_git, adj_matrix_git, static_array_git = json2graph(features_file_git, edges_file_git)

proj2recived_file = 'gid_sid_pruned.txt'
cross_data_generation(G_proj_org=G_git, adj_proj=adj_matrix_git, static_proj=static_array_git,
                      G_received_org=G_stack, adj_received=adj_matrix_stack, proj2recived_file=proj2recived_file,
                      nums=1, percentage=10, diffusion_proj='LT', diffusion_recived='IC',
                      dataset='github2stack')
