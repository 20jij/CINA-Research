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



def json2graph(orig_feature_file, target_feature_file, edge_file, hop):
    print("start")
    with open(orig_feature_file) as json_file:
        orig_static_features = json.load(json_file)
    G = nx.Graph()
    G.add_nodes_from([(node, {**attr}) for (node, attr) in orig_static_features.items()])
    df = pd.read_csv(edge_file, delim_whitespace=True, header=None)

    with open(target_feature_file) as json_file:
        target_static_features = json.load(json_file)

    connecting_target_nodes = set()
    for index, row in df.iterrows():
        source_node = row[0]
        target_node = row[1]

        # # Check if source node in 2022 and target nodes exist before 2022
        if source_node in G.nodes():
            if target_node in target_static_features:
                G.add_nodes_from([(target_node,  target_static_features[target_node])])
                G.add_edge(source_node, target_node)
                connecting_target_nodes.add(target_node)
            elif target_node in G.nodes():
                G.add_edge(source_node, target_node)

    # taking hop within target_feature_file
    print("hopping")
    # build target node graph
    G_git_target = nx.Graph()
    for target_node, features in target_static_features.items():
        G_git_target.add_nodes_from([(target_node, features)])
    for index, row in df.iterrows():
        node1 = row[0]
        node2 = row[1]
        # Check if both source node and target node in target node graph 
        if node1 in G_git_target.nodes() and node2 in G_git_target.nodes() :
            G_git_target.add_edge(node1, node2)

    final_git_nodes = []
    for node in connecting_target_nodes:
        final_git_nodes.extend(list(nx.single_source_shortest_path_length(G_git_target, node, cutoff=hop).keys()))
    final_git_nodes = list(set(final_git_nodes))  # 298285864 -> 20231
    print(len(final_git_nodes))
    # only contains the hop nodes
    G_git_target_pruned = G_git_target.subgraph(final_git_nodes)

    G_git_final = nx.compose(G, G_git_target_pruned)


    node_name_list = []
    static_features = []
    delete_node = []
    for node_name, feature_dict in list(G_git_final.nodes(data=True)):
        if len(list(feature_dict.values())[1:-1]) == 0:
            delete_node.append(node_name)
        else:
            node_name_list.append(node_name)
            # static_features.append(list(feature_dict.values())[1:-1])
            static_features.append(list(feature_dict.values())[2:-1])
    G_git_final.remove_nodes_from(delete_node)
    adj_matrix = nx.to_numpy_array(G_git_final, dtype='f')
    # print(adj_matrix.shape)
    static_array = np.asarray(static_features, dtype=np.float32)
#     nx.draw(G,with_labels=True)
#     plt.draw()
#     plt.show()
    return G_git_final, adj_matrix, static_array

def text2graph(node_file, edge_file1, edge_file2):
    if node_file !=None:
        nodes_list = pd.read_csv(node_file, delim_whitespace=True, header=None)[0].values.tolist()
        G = nx.Graph()
        G.add_nodes_from(nodes_list)
    else:
        G = nx.Graph()

    df = pd.read_csv(edge_file1, delim_whitespace=True, header=None)
    for index, row in df.iterrows():
        G.add_edge(row[0], row[1])
    df = pd.read_csv(edge_file2, delim_whitespace=True, header=None)
    for index, row in df.iterrows():
        G.add_edge(row[0], row[1])

    # adj_matrix = nx.to_numpy_array(G, dtype='f')
    # return G, adj_matrix
    return G


def stackGraph(input_git, hop):
    with open(input_git, ) as inputFile:
        sf_df = pd.read_json(inputFile, orient='index')
    # print(sf_df.head())

    sf_df.index.names = ['git_id']
    sf_df = sf_df.reset_index()
    # print(sf_df.head())
    proj2recived_file = 'gid_sid.txt'
    df_proj2recived = pd.read_csv(proj2recived_file, delim_whitespace=True, header=None)
    df_proj2recived = df_proj2recived.set_axis(['git_id', 'stack_id'], axis=1)
    # print(df_proj2recived.head())
    # GS_df = pd.merge(sf_df, df_proj2recived, on='git_id') # Keeping only the found values
    GS_df = pd.merge(sf_df, df_proj2recived, on='git_id', how='left')  # Keeping the values not found also
    GS_df['stack_id'] = GS_df['stack_id'].astype('Int64')
    # GS_df['created_at'] = pd.to_datetime(GS_df['created_at'])
    # print(GS_df.head())
    # print(len(GS_df.index))
    # print(len(GS_df[GS_df["stack_id"].isnull()].index)) # Checking the number of NaN in stack_id
    # GS_df.to_csv('../CINA_data/gitHub/stack.csv', index = True)
    GS_df[~GS_df['stack_id'].isna()][['git_id', 'stack_id']].to_csv('gid_sid_pruned.txt', sep='\t',
                                                                    index=False)
    n_cross_edges = len(GS_df[~GS_df['stack_id'].isna()][['git_id', 'stack_id']])
    # GS_df.head()
    # time_df = pd.pivot_table(GS_df, index=GS_df.created_at.dt.month, columns=GS_df.created_at.dt.year,
    #                          values='stack_id', aggfunc='sum')
    # # time_df.to_csv('../CINA_data/gitHub/stack_time.csv', index = True)
    # # time_df.plot()
    # ax_gs = GS_df.groupby(['year']).count().plot.bar(y=["git_id", "stack_id"])
    # for p in ax_gs.patches:
    #     ax_gs.annotate(f'{p.get_height():0.2f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center',
    #                 va='center', xytext=(0, 10), textcoords='offset points')
    # (GS_df['created_at'].dt.month)
    # df = pd.read_csv('sales.csv')

    # GS_df['created_at'] = pd.to_datetime(GS_df['created_at'])
    # GS_df['year'] = GS_df['created_at'].dt.year
    # GS_df['month'] = GS_df['created_at'].dt.month

    # # grouped = GS_df.groupby(['year', 'month'])
    # grouped = GS_df.groupby(['year'])
    # counts = grouped.size()
    # df_year = counts.reset_index(name='count')
    # print(df_counts)
    # df_counts.plot()
    # ax = df_year.plot.bar(x='year', rot=0, title='Distribution', figsize=(15, 10), fontsize=12)
    # # for container in ax.containers:
    # #     ax.bar_label(container)
    # # colors = ['#5cb85c', '#5bc0de', '#d9534f']
    # for p in ax.patches:
    #     ax.annotate(f'{p.get_height():0.2f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center',
    #                 va='center', xytext=(0, 10), textcoords='offset points')
    node_file_stack = 'sid_all.txt'
    edge_file_stack_1 = 'all_sid_link_edges.txt'
    edge_file_stack_2 = 'all_sid_parent_edges.txt'

    G_stack = text2graph(node_file_stack, edge_file_stack_1, edge_file_stack_2)
    stack_nodes = GS_df.loc[GS_df['stack_id'].notnull(), ['stack_id' ]]['stack_id' ].tolist()
    # print(len(stack_nodes))
    final_stack_nodes = []
    for node in set(stack_nodes):
        final_stack_nodes.extend(list(nx.single_source_shortest_path_length(G_stack, node, cutoff=hop).keys()))
    final_stack_nodes = list(set(final_stack_nodes))  # 298285864 -> 20231
    # print(len(final_stack_nodes))
    G_stack_pruned = G_stack.subgraph(final_stack_nodes)

    # print('G stack result')
    # print(len(G_stack_pruned.nodes()))
    # print(len(G_stack_pruned.edges()))

    # file_path = 'G_stack_pruned_' + str(year) + '.pkl'
    # with open(file_path, 'wb') as fp:
    #     pickle.dump(G_stack_pruned, fp)

    return G_stack_pruned, n_cross_edges
    



def generate_seed_vector(top_nodes, seed_num, G):
    seed_nodes = random.sample(top_nodes, seed_num)
    seed_vector = [1 if node in seed_nodes else 0 for node in G.nodes()]
    return seed_vector

def infected_nodes(G, seed_vector_init, inf_vec_all, diffusion='LT', diff_num = 10, iter_num = 100):
    seed_vector = [i for i in range(len(seed_vector_init)) if seed_vector_init[i] == 1]
    # print(seed_vector)
    for j in range(diff_num):
        if diffusion == 'LT':
            model = ep.ThresholdModel(G)
            config = mc.Configuration()
            for n in G.nodes():
                config.add_node_configuration("threshold", n, 0.5)
        elif diffusion == 'IC':
            model = ep.IndependentCascadesModel(G)
            config = mc.Configuration()
            for e in G.edges():
                rate = 1 / nx.degree(G)[e[1]]
                # 1 / nx.degree(G)[e[1]]
                config.add_edge_configuration("threshold", e, rate)
        elif diffusion == 'SIS':
            model = ep.SISModel(G)
            config = mc.Configuration()
            config.add_model_parameter('beta', 0.001)
            config.add_model_parameter('lambda', 0.001)
        else:
            raise ValueError('Only IC, LT and SIS are supported.')

        config.add_model_initial_configuration("Infected", seed_vector)

        model.set_initial_status(config)

        iterations = model.iteration_bunch(iter_num)

        node_status = iterations[0]['status']

        for j in range(1, len(iterations)):
            node_status.update(iterations[j]['status'])

        inf_vec = np.array(list(node_status.values()))
        inf_vec[inf_vec == 2] = 1

        inf_vec_all += inf_vec
    return inf_vec_all


def cross_data_generation(G_proj_org, adj_proj, static_proj, G_received_org, adj_received, proj2recived_file,
                          nums=100, percentage=10, diffusion_proj='LT', diffusion_recived='IC', dataset='github2stack'):
    nodes_name_G_proj = np.array(list(G_proj_org.nodes()))
    nodes_name_G_recived = np.array(list(G_received_org.nodes()))
    df_proj2recived = pd.read_csv(proj2recived_file, delim_whitespace=True, header=None)
    proj_nodes = df_proj2recived[0].to_numpy() #0
    receipient_nodes = df_proj2recived[1].to_numpy()#1

    # G_proj = nx.from_numpy_matrix(adj_proj)
    G_proj = nx.DiGraph(adj_proj)

    
    node_num_proj = len(G_proj.nodes())
    seed_num_proj = int(percentage * node_num_proj / 100)
    samples_proj = []

    degree_list_proj = list(G_proj.degree())
    degree_list_proj.sort(key=lambda x: x[1], reverse=True)
    top_nodes_proj = [x[0] for x in degree_list_proj[:int(len(degree_list_proj) * 0.25)]]

    G_received = nx.DiGraph(adj_received)
    node_num_received = len(G_received.nodes())
    # seed_num_received = int(percentage * node_num_received / 100)
    samples_received = []

    for j in range(nums):
        print('Sample {} generating'.format(j))
        seed_vector_proj = generate_seed_vector(top_nodes_proj, seed_num_proj, G_proj)
        inf_vec_all_proj = torch.zeros(node_num_proj)
        inf_vec_all_proj = infected_nodes(G_proj, seed_vector_proj, inf_vec_all_proj, diffusion=diffusion_proj,
                                          diff_num=10, iter_num=100)
        inf_vec_all_proj = inf_vec_all_proj / 10  # divided by the diffusion_num
        samples_proj.append([seed_vector_proj, inf_vec_all_proj])

        print(len(inf_vec_all_proj))
        print(inf_vec_all_proj)

        # Find the final infected index in the projection network, and use it to find the seed infected nodes in the receiving network. 
        inf_proj_idx = []
        # i is name of the infected notes in projection
        for i in nodes_name_G_proj[inf_vec_all_proj == 1]:
            print(i)
            inf_proj_idx.extend(np.where(proj_nodes == i)[0].tolist())
        # seed_name_received = nodes_name_G_recived[inf_proj_idx]
        seed_name_received = receipient_nodes[inf_proj_idx]

        # convert to integer!!
        seed_name_received = list(map(int, seed_name_received))


        # print("check stack seed node")
        # print(seed_name_received)
        # print(len(seed_name_received))


        seed_vector_received = []
        for index, element in enumerate(nodes_name_G_recived):
            # print(type(element))
            # print(element)
            seed_vector_received.append(1) if element in seed_name_received else seed_vector_received.append(0)
        inf_vec_all_received = torch.zeros(node_num_received)
        inf_vec_all_received = infected_nodes(G_received, seed_vector_received, inf_vec_all_received,
                                              diffusion=diffusion_recived, diff_num=10, iter_num=100)
        inf_vec_all_received = inf_vec_all_received / 10  # divided by the diffusion_num

        # print("check stack seed node vector")
        # print(seed_vector_received)
        # print(len(seed_vector_received))

        # print("check stack all infected node")
        # print(inf_vec_all_received)
        # print(len(inf_vec_all_received))
        samples_received.append([seed_vector_received, inf_vec_all_received])

    samples_proj = torch.Tensor(samples_proj).permute(0, 2, 1)  ## Why permutation: Changing shape from [samples, 2, nodes] to [samples, nodes, 2]
    samples_received = torch.Tensor(samples_received).permute(0, 2, 1)  ## Why permutation

    data_dict = {'original_graph_proj': G_proj_org,
                 'adj_proj': adj_proj,
                 'prob_proj': adj_proj,
                 'inverse_pairs_proj': samples_proj,
                 'static_features_proj': static_proj,
                 'proj_nodes': proj_nodes,
                 'original_graph_received': G_received_org,
                 'adj_received': adj_received,
                 'prob_received': adj_received,
                 'inverse_pairs_received': samples_received,
                 'receipient_nodes': receipient_nodes}

    # rate = 0.8
    f = open('{}_{}2{}_{}_{}_top_0.25.SG'.format(dataset, diffusion_proj, diffusion_recived, percentage, nums), 'wb')
    pickle.dump(data_dict, f)
    f.close()
    print('Data generation finished')