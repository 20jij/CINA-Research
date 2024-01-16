
import sys
import re
# import igraph as ig
# import matplotlib.pyplot as plt


sys.setrecursionlimit(10000000)

freq_graph = {}
repo_id_graph = {}
count_repo = 0

input_file = '/Users/jasonji/Desktop/CINA/code/graph_building/all/data/dependency_data_d1.txt'

# build database
with open(input_file) as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        
        if line=='\n' or len(line)==0:
            continue
        splits = line.split(' ')
        repo = ''
        if len(splits)==2:
            repo = splits[0][:-1]
        elif len(splits) == 3:
            repo = splits[2]

        # double check 
        match = re.findall('https://github\.com/[^"].+', repo)
        if len(match)==0:
            continue

        # # record repo frequency
        # if repo not in freq_graph:
        #     freq_graph[repo] = 0
        # freq_graph[repo]+=1

        # assign id to repo
        g_id = 'g'+ str(count_repo)
        if repo not in repo_id_graph:
            repo_id_graph[repo] = g_id
            count_repo+=1



# # write id and edge graph to txt files
# with open('/Users/jasonji/Desktop/CINA/code/graph_building/all/data/repo_id.txt', 'a+') as f:
#     for repo,gid in repo_id_graph.items():
#         line = repo + " " + gid + "\n"
#         f.write(line)

# build edge graph
# graph structure: if repo A depends on repo B, B -> A
edge_graph = {}
with open(input_file) as f:
    lines = f.readlines()
    i = 0
   
    # ONLY READ 400,125 LINES FIRST, ABOUT 1/2 OF ALL DATA
    while i < len(lines):
        if i%1000 == 0:
            print(i)
        line = lines[i].strip()
        if line=='\n' or len(line)==0:
            i+=1
            continue
        splits = line.split(' ')
        # repo A
        if len(splits)==2:
            repo_A = splits[0][:-1]
            # double check 
            match = re.findall('https://github\.com/[^"].+', repo_A)
            if len(match)==0:
                i+=1
                continue
            gid_A = repo_id_graph[repo_A]
            # repo B
            i+=1
            line = lines[i]
            while len(line)!=0 and i<len(lines):
                line = lines[i].strip().replace("\n", "")
                splits = line.split(' ')
                
                # double check for erroneous data
                if len(splits)<3:
                    i+=1
                    continue

                repo_B = splits[2]
                repo_B = repo_B.strip('\n')
                match = re.findall('https://github\.com/[^"].+', repo_B)
                if len(match)==0:
                    i+=1
                    continue

                gid_B = repo_id_graph[repo_B]
                if gid_B not in edge_graph:
                    edge_graph[gid_B] = set()
                edge_graph[gid_B].add(gid_A)
                i+=1       
        i+=1



# edge file format: repoB repoA
with open('/Users/jasonji/Desktop/CINA/code/graph_building/all/data/edges.txt', 'a+') as f:
    for vert1, vert2_list in edge_graph.items():
        for vert2 in vert2_list:
            line = vert1 + " " + vert2 + "\n"
            f.write(line)




# # count_f= 0
# # for v in freq_graph.values():
# #     if v>1:
# #         count_f+=1

# # edge_count = 0
# # for vert1, vert2_list in edge_graph.items():
# #     for vert2 in vert2_list:
# #         edge_count+=1

# # print(count_repo,count_f,len(edge_graph.keys()),edge_count)




# # # visualization
# # n_vertices = count_repo
# # edges = []

# # for vert1, vert2_list in edge_graph.items():
# #     # remove g from id 
# #     temp = vert1[1:]
# #     for vert2 in vert2_list:
# #         edge = (int(temp), int(vert2[1:]))
# #         edges.append(edge)
# # print(edges)

# # g = ig.Graph(n_vertices, edges, directed=True)

# # # create name, depth lable
# # for i in range(n_vertices):
# #     gid = 'g' + str(i)
# #     g.vs[i]["name"] = gid
# #     if gid in edge_graph.keys():
# #         g.vs[i]["depth"] = 1
# #     else:
# #         g.vs[i]["depth"] = 0

# # # Set attributes for the graph, nodes, and edges
# # g["title"] = "Sample Graph"
# # # Plot in matplotlib
# # fig, ax = plt.subplots(figsize=(7,7))
# # ig.plot(
# #     g,
# #     target=ax,
# #     vertex_size=0.5,
# #     vertex_color=["steelblue" if depth == 1 else "salmon" for depth in g.vs["depth"]],
# #     vertex_label=g.vs["name"],
# #     vertex_label_size=7.0,
# # )
# # plt.show()




        