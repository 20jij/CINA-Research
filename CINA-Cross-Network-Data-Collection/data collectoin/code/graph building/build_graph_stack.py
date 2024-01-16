import sys
import re
# import igraph as ig
# import matplotlib.pyplot as plt
import json
from collections import defaultdict


sys.setrecursionlimit(100000)

# initialize github repo-id graph
repo_gid_graph = {}
with open('/Users/jasonji/Desktop/CINA/code/graph_building/all1/repo_id.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip().split(" ")
        repo_gid_graph[line[0]] = line[1]


# build github_id to stackoverflow post_id adjacency list
# CAN JUST USE clean_links1.json INSTEAD 
gid_sid_graph = {}

json_file_path = '/Users/jasonji/Desktop/CINA/data/Github/clean_links1.json'
with open(json_file_path, 'r') as json_file:
    repo_sid = json.load(json_file)

all_sid = set()
not_included = []

for item in repo_sid:
    repo = item.get('link')
    sid = item.get('id')
    if repo and sid:
        if repo not in repo_gid_graph:
            not_included.append(repo)
            continue
        gid = repo_gid_graph[repo]
        gid_sid_graph[gid] = sid
        all_sid.add(sid)


# # write gid-sid adjacency list to a txt file
# with open('/Users/jasonji/Desktop/CINA/code/graph_building/all1/gid_sid.txt', 'a+') as f:
#     for gid,sid in gid_sid_graph.items():
#         line = gid + " " + sid + "\n"
#         f.write(line)

# print(len(not_included))


# # build edges by finding parent(question post) of the linked posts
# # currently just have the sid, not the full data (on the server)
# # graph structure: sid(answer) -> sid(parent/question)
# edge_graph = defaultdict(set)
# vertices = set()
# with open('/Users/jasonji/Desktop/CINA/code/graph_building/linked_posts.json') as f:
#     data = json.loads(f.read())
#     for d in data:
#         vertices.add(d["Id"])
#         if d["PostTypeId"] == "2":
#             edge_graph[d["Id"]].add(d["ParentId"])
#             vertices.add(d["ParentId"])

# # write edge graph to txt file 
# # edge file format: sid(answer) sid(parent/question)
# # with open('/Users/jasonji/Desktop/CINA/code/graph_building/sid_edges.txt', 'a+') as f:
# #     for sid1, sid2 in edge_graph.items():
# #         line = sid1 + " " + sid2 + "\n"
# #         f.write(line)

# # add linked post realtionship to edges as well
# with open('/Users/jasonji/Desktop/CINA/code/graph_building/sid_link_edges.txt') as f:
#     lines = f.readlines()
#     for line in lines:
#         sid, sid_l, type = line.strip().split(" ")
#         vertices.add(sid)
#         vertices.add(sid_l)
#         edge_graph[sid].add(sid_l)

# # add edges within subgraph (two linked posts are linked to each other)
# with open('/Users/jasonji/Desktop/CINA/code/graph_building/subgraph_edges.txt') as f:
#     lines = f.readlines()
#     for line in lines:
#         sid, sid_l, type = line.strip().split(" ")
#         vertices.add(sid)
#         vertices.add(sid_l)
#         edge_graph[sid].add(sid_l)



# # build PostsLinks edges


# # get the linked stackoverflow posts
# stack_data = []
# with open('/Users/jasonji/Desktop/CINA/data/StackOverflow/complete_linked_posts.json') as f:
#     data = json.loads(f.read())
#     for d in data:
#         # if d["Id"] in all_sid:
#         stack_data.append(d)

# print(len(stack_data))
# # wrote into a json file
# with open("linked_posts.json","a") as f:
#     json.dump(stack_data,f,indent=4)
   


# # visualization for stackoverflow network
# n_vertices = len(vertices)
# # need to rename sid to start consecutively from 0
# vert_vert0 = {}
# vert0_vert = {}
# count = 0
# for vert in vertices:
#     vert_vert0[vert] = count
#     vert0_vert[count] = vert
#     count+=1

# edges = []
# for vert1, vert2_list in edge_graph.items():
#     for vert2 in vert2_list:
#         edge = (int(vert_vert0[vert1]), int(vert_vert0[vert2]))
#         edges.append(edge)

# g = ig.Graph(n_vertices, edges, directed=True)

# # create name, parent lable
# for i in range(n_vertices):
#     v_name = vert0_vert[i]
#     g.vs[i]["name"] = v_name
#     if v_name in all_sid:
#         g.vs[i]["bridge"] = 1
#     else:
#         g.vs[i]["bridge"] = 0
    

# # Set attributes for the graph, nodes, and edges
# g["title"] = "Sample Graph"
# # Plot in matplotlib
# fig, ax = plt.subplots(figsize=(7,7))
# ig.plot(
#     g,
#     target=ax,
#     vertex_size=0.2,
#     vertex_color=["steelblue" if bridge == 1 else "salmon" for bridge in g.vs["bridge"]],
#     vertex_label=g.vs["name"],
#     vertex_label_size=7.0,
# )
# plt.show()



# # visualization for entire graph
# gid_set = set()
# edge_graph_g = {}
# with open("gid_edges.txt") as f:
#     lines = f.readlines()
#     for line in lines:
#         line = line.strip().split(" ")
#         gid_set.add(line[0])
#         gid_set.add(line[1])
#         if line[0] not in edge_graph_g:
#             edge_graph_g[line[0]] = []
#         edge_graph_g[line[0]].append(line[1])

# sid_set = set()
# for sid1, sid2_l in edge_graph.items():
#     sid_set.add(sid1)
#     for sid2 in sid2_l:
#         sid_set.add(sid2)

# n_vertices = len(gid_set) + len(sid_set)
# # need to rename sid to start consecutively from the end of gid
# vert_vert0 = {}
# vert0_vert = {}
# count = len(gid_set)
# for vert in vertices:
#     vert_vert0[int(vert)] = count
#     vert0_vert[count] = int(vert)
#     count+=1

# edges = []
# # github edges
# for vert1, vert2_l in edge_graph_g.items():
#     # remove g from id 
#     for vert2 in vert2_l:
#         edge = (int(vert1[1:]), int(vert2[1:]))
#         edges.append(edge)
# # stackoverflow edges
# for vert1, vert2_list in edge_graph.items():
#     for vert2 in vert2_list:
#         edge = (int(vert_vert0[int(vert1)]), int(vert_vert0[int(vert2)]))
#         edges.append(edge)
# # bridging edges
# with open("/Users/jasonji/Desktop/CINA/code/graph_building/gid_sid.txt") as f:
#     lines = f.readlines()
#     for line in lines:
#         line = line.strip().split(" ")
#         gid = line[0]
#         sid = line[1]
#         edge = (int(gid[1:]),int(vert_vert0[int(sid)]))
#         edges.append(edge)



# g = ig.Graph(n_vertices, edges, directed=True)

# # create name, color, depth, parent lable
# for i in range(len(gid_set)):
#     gid = 'g' + str(i)
#     g.vs[i]["name"] = gid
#     if gid in edge_graph_g.keys():
#         g.vs[i]["depth"] = 1
#         g.vs[i]['color'] = "steelblue"
#     else:
#         g.vs[i]["depth"] = 0
#         g.vs[i]['color'] = "salmon"
# for i in range(len(gid_set),n_vertices):
#     v_name = str(vert0_vert[i])
#     g.vs[i]["name"] = v_name
#     if v_name in all_sid:
#         g.vs[i]["bridge"] = 1
#         g.vs[i]['color'] = "red"
#     else:
#         g.vs[i]["bridge"] = 0
#         g.vs[i]['color'] = "green"


# # Set attributes for the graph, nodes, and edges
# g["title"] = "Sample Graph"
# # Plot in matplotlib
# fig, ax = plt.subplots(figsize=(7,7))
# ig.plot(
#     g,
#     target=ax,
#     vertex_size=0.5,
#     # vertex_color=["red" if parent == 1 else "green" for parent in g.vs["parent"]],
#     # vertex_color=["steelblue" if depth == 1 else "salmon" for depth in g.vs["depth"]],
#     vertex_label=g.vs["name"],
#     vertex_label_size=7.0,
# )
# plt.show()


        


