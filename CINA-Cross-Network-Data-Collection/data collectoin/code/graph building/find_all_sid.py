# find all sid existed 


sid_set = set()
with open('/Users/jasonji/Desktop/CINA/code/graph_building/all/data/all_sid_link_edges.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip().split(' ')
        sid_set.add(line[0])
        sid_set.add(line[1])
with open('/Users/jasonji/Desktop/CINA/code/graph_building/all/data/all_sid_parent_edges.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip().split(" ")
        sid_set.add(line[0])
        sid_set.add(line[1])

with open('/Users/jasonji/Desktop/CINA/code/graph_building/all/data/gid_sid.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip().split(" ")
        sid_set.add(line[1])

print(len(sid_set))
with open('/Users/jasonji/Desktop/CINA/code/graph_building/all/data/sid_all.txt', 'w') as f:
        for sid in sid_set:
            line = sid + "\n"
            f.write(line)

