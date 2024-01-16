# This script finds stars, contributors, forks, and watchers of github repos

import github_api
import json
import time 
import sys
import requests

# function to add to JSON 
# everytime gets the current list, extend it, and dump it again.
def write_json(new_data, output_f):
    with open(output_f,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data.extend(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
 
# find the author and repo name if exists in the link
# NEED TO CONSIDER ONLY AUTHOR CASE TO FIND ITS FOLLOWERS -- Maybe a seperate file!!!
def find_author_repo(link):
    splits = link.split('/')
    # return None if the link doesn't specify repo
    # ex. https://github.com/unittest-cpp
    if len(splits) <= 4:
        return None
    author = splits[3].strip('\n')
    repo = splits[4].strip('\n')
    return [author,repo]


def collect_data(input_f, output_f):
    # data store the current list of dictionaries (Each represents a repo and its connections)
    data = []

    # create the json file
    # with open("../data/Github/github_data2.json","a") as f:
    #     json.dump(data,f)

    f = open(input_f)
    links = json.load(f)
    f.close()

    count = 0

    # locate the starting link position based on the length of the output file
    index_start = 84430

    # with open(output_f) as file:
    #     data = json.load(file)
    #     index_start += len(data)
        # print(len(data))
        # print(data[-1])
    
    print(index_start)
    # print(len(links))
    # print(links[index_start])
    # exit()

    # initialize Github_API object with rotating proxy
    proxies={
        "http": "http://wfietgbd-rotate:ish8sg8dlu4x@p.webshare.io:80/",
        "https": "http://wfietgbd-rotate:ish8sg8dlu4x@p.webshare.io:80/"
    }
    minner = github_api.GitHub_API(proxies)

    for i in range(index_start,len(links)):
        print(i)
        entry = links[i]

        # write data every 10 github links
        if count == 10:
            write_json(data,output_f)
            # reset the data and count
            data = []
            count = 0

        link = entry['link'].strip('\n')
        print(link)
        id = entry['id']
        
        # parse the link and find its author and reppo
        author_repo = find_author_repo(link)
        # double check if author and repo are valid
        if not author_repo or not author_repo[0] or not author_repo[1]:
            continue
        author, repo = author_repo

        try:
            # call functions to find its github connections
            forks = minner.find_forks(author, repo)
            # if invalid link, don't need to call the rest of functions via github api
            if not forks:
                # still count the number of api calls
                count+=1
                continue
            watchers = minner.find_watchers(author, repo)
            stars = minner.find_stargazers(author, repo)
            contributors = minner.find_contributors(author,repo)
            # store the data
            link_object = {}
            link_object['repo_link'] = link
            # this is its corresponding stackoverflow id
            link_object['stack_id'] = id
            link_object['forks'] = forks
            link_object['watchers'] = watchers
            link_object['stars'] = stars
            link_object['contributors'] = contributors

            # store link and its connections into data
            data.append(link_object)

            count += 1

        except:
            count +=1

       
        # for testing
        # if count > 3:
        #     break

    # print(data)

    # dump the remaining data
    write_json(data,output_f)

def main():
    # argument format: 
    # [input file (stores the original repo links)] [output file (stores the repo links and its forks, stars, and watchers)] [proxy]
    # current default:
    input_f = '../data/Github/no_dup_links.json'
    output_f = '../data/Github/github_data2.json'
    for i, arg in enumerate(sys.argv):
        if i == 0:
            continue
        if i == 1:
            input_f = arg
        if i == 2:
            output_f = arg
        if i == 3:
            proxy = arg
            
    collect_data(input_f,output_f)



if __name__ == '__main__':
    main()
    

