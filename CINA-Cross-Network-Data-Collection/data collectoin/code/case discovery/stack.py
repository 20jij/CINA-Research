# investigate found github repos and find corresponding stackoverflow posts

import json


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


stack_id = [37993157,42622465,44688478,45080979,51488893,56832383,58861972,65492575,68519915,69144016,70324362,72875597]
stack_id = set([str(id) for id in stack_id])

stack_id_post = {}
with open('/Users/jasonji/Desktop/CINA/data/StackOverflow/complete_linked_posts.json') as f:
    file = json.load(f)
    for post in file:
        sid = post["Id"]
        if sid in stack_id:
            stack_id_post[sid] = post
    
with open("stack_posts.json", "w") as outfile:
    json.dump(stack_id_post, outfile, indent = 4)
print(stack_id_post)


