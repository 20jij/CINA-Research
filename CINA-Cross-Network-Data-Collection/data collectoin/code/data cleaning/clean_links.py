# this code removes duplicates github links

import json

def find_author_repo(link):
    splits = link.split('/')
    # return None if the link doesn't specify repo
    # ex. https://github.com/unittest-cpp
    if len(splits) <= 4:
        return None
    author = splits[3].strip('\n')
    repo = splits[4].strip('\n')
    return [author,repo]



f = open('../data/Github/new_extracted_links.json')
original = json.load(f)
f.close()

new = []
track = set()


for entry in original:
    link = entry['link']

    author_repo = find_author_repo(link)

    # remove links that don't sepecify both repo and author
    if not author_repo or not author_repo[0] or not author_repo[1]:
        continue

    author_repo = author_repo[0]+author_repo[1]

    # # remove duplicates
    # if author_repo in track:
    #     continue
    
    # add to track and the new json file
    track.add(author_repo)
    new.append(entry)



print(len(track))
print(len(new))
with open("../data/Github/clean_links1.json","w") as f:
        json.dump(new,f, indent=4)

    