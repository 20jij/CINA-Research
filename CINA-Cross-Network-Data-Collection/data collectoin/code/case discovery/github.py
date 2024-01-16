# find cases of github projects that contains misinformation in the minned social network

import re

# collect all buggy github repos
links = set()
packages = set()

with open('buggy_project_information.txt', '+r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip().split('\t')
        links.add(line[0].strip())
        packages.add(line[1].strip())

# find github posts that contain these buggy repo
cases = []
with open('/Users/jasonji/Desktop/CINA/code/dependency_data_d1.txt') as f:
    lines = f.readlines()
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
            if repo in links:
                cases.append((repo,sid))
            
        elif len(splits)==3:
            package = splits[1][:-1]
            repo = splits[2]
            # double check 
            match = re.findall('https://github\.com/[^"].+', repo)
            if len(match)==0:
                continue
            if repo in links or package in packages:
                cases.append((repo,package))

print(cases)
cases = [('https://github.com/apache/storm.git', '31782408'), 
         ('https://github.com/chrismattmann/tika-python', 'tika'), 
         ('https://github.com/chrismattmann/tika-python', 'tika'), 
         ('https://github.com/chrismattmann/tika-python', 'tika'), 
         ('https://github.com/chrismattmann/tika-python', 'tika'), 
         ('https://github.com/chrismattmann/tika-python', 'tika'), 
         ('https://github.com/chrismattmann/tika-python', 'tika'), 
         ('https://github.com/chrismattmann/tika-python', 'tika'), 
         ('https://github.com/chrismattmann/tika-python', 'tika'), 
         ('https://github.com/chrismattmann/tika-python', 'tika'), 
         ('https://github.com/apache/jena.git', '71726949'), 
         ('https://github.com/apache/httpcomponents-core.git', '72524977'), 
         ('https://github.com/kiegroup/drools.git', '73598095')]
