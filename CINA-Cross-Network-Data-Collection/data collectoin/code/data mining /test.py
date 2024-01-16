import github_api 
import json
# import xkcd2347
from xkcd2347_copy import * 

sys.setrecursionlimit(100000)


def find_author_repo(link):
    splits = link.split('/')
    # return None if the link doesn't specify repo
    # ex. https://github.com/unittest-cpp
    if len(splits) <= 4:
        return None
    author = splits[3].strip('\n')
    repo = splits[4].strip('\n')
    return [author,repo]


# output_repos = set()
# input_repos = set()

# with open('../data/Github/github_data1.json') as f:
#     data = json.load(f)
#     for entry in data:
#         repo = entry['repo_link']
#         output_repos.add(repo)

# with open('../data/Github/no_dup_links.json') as f:
#     data = json.load(f)
#     for i in range(0, 120000):
#         entry = data[i]
#         link = entry['link']
#         if link=='https://github.com/darrylb123/u':
#             print(i)
#             exit()


proxies={
    "http": "http://wfietgbd-rotate:ish8sg8dlu4x@p.webshare.io:80/",
    "https": "http://wfietgbd-rotate:ish8sg8dlu4x@p.webshare.io:80/"
}

username="20jij"
token=""



minner = github_api.GitHub_API(proxies)


try:
   
    # #change the url to https://httpbin.org/ip that doesnt block anything
    # r = requests.get('https://httpbin.org/ip', proxies=proxies,timeout=10)
    # print(r.json(), r.status_code)

    link = 'https://github.com/darrylb123/u'
    author,repo_name = find_author_repo(link)
    print(minner.find_forks(author, repo_name))
    # url = "https://api.github.com/repos/" + author + "/" + repo_name + "/forks?per_page=100&page=1" 
    # response = requests.get(url, auth =(username, token), proxies=proxies)
    # status = response.status_code
    # print(status)
    # print(response.json())
except requests.ConnectionError as err:
    print(repr(err))    


