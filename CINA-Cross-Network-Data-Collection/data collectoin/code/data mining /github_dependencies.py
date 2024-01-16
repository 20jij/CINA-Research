# import xkcd2347
from xkcd2347_copy import * 

import json
import sys

sys.setrecursionlimit(10000)

token = ""

# uses modiefied tool 
gh = GitHub(key=token)
# gh = xkcd2347.GitHub(key=token)

# only the first level
depth = 1


def find_author_repo(link):
    splits = link.split('/')
    # return None if the link doesn't specify repo
    # ex. https://github.com/unittest-cpp
    if len(splits) <= 4:
        return None
    author = splits[3].strip('\n')
    repo = splits[4].strip('\n')
    return [author,repo]



f = open('../data/Github/clean_links1.json')
links = json.load(f)
f.close()

# read the previously visited repo
# gh.get_visited("visited_repo.json")

# print(len(links))
# exit()
# 925422
for i in range(925422, 925423):
    print(i)
    link = links[i]['link']
    id = links[i]['id']

    with open("dependency_data_new.txt", 'a') as file:
        # print(f"\n{link}, {id}\n")
        file.write(f"\n{link}, {id}\n")
    
        # parse the link and find its author and reppo
        author_repo = find_author_repo(link)
        # double check if author and repo are valid
        if not author_repo or not author_repo[0] or not author_repo[1]:
            continue
        author, repo = author_repo

        try:
            for dep in gh.get_dependencies(author, repo, depth):
                if not dep:
                    continue
                level = dep['level']
                package = dep['packageName']
                if dep['repository']:
                    url = 'https://github.com/{0[owner][login]}/{0[name]}'.format(dep['repository'])
                else:
                    url = ''
                # print('{} {}: {}'.format(url))


                file.write('{}\n'.format(url))
                # print(f"{level} {package}{repo_owner}")
                # gh.write_visited("visited_repo.json")

        
        except Exception as e:
            print(e)
            file.write(f" \n")
            continue

        file.write(f" \n")
    # write the new visited repo
    # gh.write_visited("visited_repo.json")

    