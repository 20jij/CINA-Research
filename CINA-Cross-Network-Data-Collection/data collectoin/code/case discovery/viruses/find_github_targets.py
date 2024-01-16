# find cases of github projects that contains misinformation in the minned social network
import json
import re

year = 2002

while year < 2018:
    if year == 2003 or year == 2005:
        year+=1
        continue
    input_file = '/Users/jasonji/Desktop/CINA/code/case_discovery/viruses/2002-2017/' + str(year) + '_github_urls.txt'
    github_urls = set()
    with open(input_file, 'r') as input_file:
        for line in input_file:
            url = line.strip()
            if re.match(r'^https?://github\.com/', url):
                github_urls.add(url)

    print(len(github_urls))
    # find github posts that contain these buggy repo
    cases = []
    depth_0_count = 0
    depth_1_count = 0

    visited =set()

    with open('/Users/jasonji/Desktop/CINA/code/dependency_data_d1.txt') as f:
        lines = f.readlines()
        parent_repo = ''
        parent_id = 0
        for line in lines:
            line = line.strip()
            if line=='\n' or len(line)==0:
                continue
            splits = line.split(' ')

            if len(splits)==2:
                repo = splits[0][:-1]
                sid =  splits[1]
                # double check 
                match = re.findall('https://github\.com/[^"].+', repo)
                if len(match)==0:
                    continue
                if repo in github_urls:
                    cases.append((repo,sid))
                    visited.add(repo)
                    depth_0_count+=1

                parent_repo = repo
                parent_id = sid
                
            elif len(splits)==3:
                package = splits[1][:-1]
                repo = splits[2]
                # double check 
                match = re.findall('https://github\.com/[^"].+', repo)
                if len(match)==0:
                    continue
                if repo in github_urls:
                    cases.append((repo,parent_repo,parent_id))
                    visited.add(repo)
                    depth_1_count+=1
    # print(cases)
    print(len(cases),depth_0_count,depth_1_count)
    print(len(visited))
    out_file_name = '/Users/jasonji/Desktop/CINA/code/case_discovery/viruses/2002-2017/target_repo_' + str(year) +'.txt'
    with open(out_file_name, 'w') as f:
        for entry in visited:
            line = entry + '\n'
            f.write(line)
    year+=1


    # locate cases in stackoverflow network


    # stack_id_post = {}
    # with open('/Users/jasonji/Desktop/CINA/data/StackOverflow/complete_linked_posts.json') as f:
    #     file = json.load(f)
    #     for post in file:
    #         sid = post["Id"]
    #         if sid in stack_id:
    #             stack_id_post[sid] = post
