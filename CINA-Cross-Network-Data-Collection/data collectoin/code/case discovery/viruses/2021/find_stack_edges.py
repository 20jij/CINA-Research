sid_edges = {}

with open('/Users/jasonji/Desktop/CINA/code/graph_building/all/data/all_sid_parent_edges.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip().split(' ')
        if line[0] not in sid_edges:
            sid_edges[line[0]] = []
        if line[1] not in sid_edges:
            sid_edges[line[1]] = []
        sid_edges[line[0]].append(line[1])
        sid_edges[line[1]].append(line[0])

with open('/Users/jasonji/Desktop/CINA/code/graph_building/all/data/all_sid_link_edges.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip().split(" ")
        if line[0] not in sid_edges:
            sid_edges[line[0]] = []
        if line[1] not in sid_edges:
            sid_edges[line[1]] = []
        sid_edges[line[0]].append(line[1])
        sid_edges[line[1]].append(line[0])

remains_sid = ['391005', '15920472', '26486476', '58540183', '70273669']
visited = set()
output = set()

while remains_sid:
    curr_sid = remains_sid.pop()
    if curr_sid in visited:
        continue
    visited.add(curr_sid)
    if curr_sid in sid_edges:
        connected_sids = sid_edges[curr_sid]
        for connected_sid in connected_sids:
            remains_sid.append(connected_sid)
            output.add(tuple(sorted([int(curr_sid), int(connected_sid)])))


with open("html2pdf_stack_edges.txt", "w") as f:
    for edge in output:
        line = str(edge[0])+ ", " + str(edge[1]) + "\n"
        f.write(line)
print(output)