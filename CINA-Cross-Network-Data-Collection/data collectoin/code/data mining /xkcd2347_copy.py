# add visited dictionary to keep track of all the visited repos

#!/usr/bin/env python3

import os
import sys
import time
# import yaml
import shutil
import pathlib
import argparse
import requests
# import diskcache

import json

from retry import retry


class GitHub:

    def __init__(self, key, cache=None):
        self.key = key
        self.cache = cache
        self.parents = []
        # keep track of all the previously visited repo
        self.visited = {}
        self.large_dependency_threshold = 40
        self.large_dependency_repo = set()

    def get_visited(self, file):
        with open(file) as json_file:
            file_data = json.load(json_file)
            if len(file_data)!=0:
                self.visited = file_data


    def write_visited(self, file):
        with open(file, 'w') as outfile:
            json.dump(self.visited, outfile, indent = 4)


    def get_dependencies(self, repo_owner, repo_name, depth=1, lang=None):

        # track large dependency repo
        if '{}/{}'.format(repo_owner,repo_name) in self.large_dependency_repo:
            return None

        q = '''
            {
              repository(owner: "%s", name: "%s") {
                description
                dependencyGraphManifests(first: 100) {
                  nodes {
                    blobPath
                    dependencies {
                      nodes {
                        packageName
                        repository {
                          name
                          nameWithOwner
                          owner {
                            login
                          }
                          primaryLanguage {
                            name
                          }
                        }
                        requirements
                        hasDependencies
                      }
                    }
                    dependenciesCount
                    exceedsMaxSize
                    parseable

                  }
                }
              }
            }
            '''

        # seen is used to prevent a given dependency from being reported more than
        # one when a project have multiple dependencyGraphManifests
        seen = set()

        try:
            results = self.query(q % (repo_owner, repo_name), count=0) 

        # if query can't be runned with given information, return None instead of raising exception
        # to allow algorithm to continue

        # value error means there exists a lare dependency repo
        except ValueError as ve:
            print("Encounter repo with large dependency {}/{}".format(repo_owner,repo_name))
            self.large_dependency_repo.add('{}/{}'.format(repo_owner,repo_name))
            return None
        
        except Exception as e:
            print(e)
            return None
        else: 
            if not results:
                return None
            if 'errors' in results and len(results['errors']) > 0:
                return None
                # raise Exception('\n'.join([e['message'] for e in results['errors']]))
                # sys.exit('\n'.join([e['message'] for e in results['errors']]))

            for m in results['data']['repository']['dependencyGraphManifests']['nodes']:

                
                for dep in m['dependencies']['nodes']:
                    dep['level'] = len(self.parents)

                    if lang and dep['repository'] and dep['repository']['primaryLanguage'] and dep['repository']['primaryLanguage']['name'].lower() != lang.lower():
                        continue

                    # store the repo info as dep_id in visited and parents
                    owner = ""
                    repo = ""
                    if dep['repository']:
                        owner = dep['repository']['owner']['login']
                        repo =  dep['repository']['name']
                    dep_id = '{}/{}'.format(
                            owner,
                            repo
                        )
                    
                    # track visited
                    # if dep_id in self.visited:
                    #     continue
                    # self.visited[dep_id] = 1
                
                    # track seen
                    if dep_id in seen:
                        continue
                    seen.add(dep_id)

                    yield dep

                    if (depth == 0 or len(self.parents) + 1 < depth) and dep['hasDependencies'] == True and dep['repository']:
                        dep_id = '{}/{}'.format(
                            dep['repository']['owner']['login'],
                            dep['repository']['name']
                        )
                        # prevent an infinite loop from circular dependencies
                        if dep_id not in self.parents:
                            self.parents.append(dep_id)
                            yield from self.get_dependencies(
                                dep['repository']['owner']['login'],
                                dep['repository']['name'],
                                depth,
                                lang
                            )
                            self.parents.pop()


    def query(self, q, count):
        # if it takes too much time generating the dependency info for a repo, marks it as large_dependency and skips it.
        if count > 40:
            raise ValueError("Encounter a large dependency repo when running query {}".format(q))
        if self.cache and q in self.cache:
            return self.cache[q]
        else:
            headers = {
                "Authorization": "Bearer {}".format(self.key),
                "Accept": "application/vnd.github.hawkgirl-preview+json"
            }
            resp = requests.post('https://api.github.com/graphql', json={'query': q}, headers=headers)
            
            print(resp.status_code)

            if resp.status_code == 200:
                data = resp.json()

                if 'errors' in data and len(data['errors']) > 0:
                    # this seems to happen when GitHub needs to populate the data
                    if data['errors'][0]['message'] in ['loading', 'timedout']:
                        time.sleep(5)
                        return self.query(q, count+1)
                    else:
                        return data
                elif self.cache is not None:
                    self.cache[q] = data
                    return data
                else:
                    return data

            else:
                raise Exception("Query failed to run by returning code of {}. {}".format(resp.status_code, q))



# def main():
#     argp = argparse.ArgumentParser(description="Find project dependencies using GitHub's API")
#     argp.add_argument('repository', help='The repository name e.g. jupyter/notebook')
#     argp.add_argument('--depth', type=int, default=1, help='Depth to search')
#     argp.add_argument('--lang', help='Limit to language dependencies')
#     argp.add_argument('--flush', action="store_true", help='Flush the cache of previous data')
#     args = argp.parse_args()

#     parts = args.repository.split('/')
#     if len(parts) != 2:
#         argp.error("The GitHub repository must look like jupyter/notebook")
#     repo_owner, repo_name = parts

#     config = get_config(args.flush)

#     gh = GitHub(key=config['github_token'], cache=config['cache'])
#     for dep in gh.get_dependencies(repo_owner, repo_name, depth=args.depth, lang=args.lang):
#         indent = dep['level'] * " "
#         package = dep['packageName']
#         if dep['repository']:
#             url = 'https://github.com/{0[owner][login]}/{0[name]}'.format(dep['repository'])
#         else:
#             url = ''
#         print('{} {}: {}'.format(indent, package, url))

# def get_config(flush_cache=False):
#     home = pathlib.Path.home() / ".xkcd2347"
#     cache = home / "cache"

#     if not home.exists():
#         home.mkdir()
#         cache.mkdir()

#     if flush_cache:
#         shutil.rmtree(cache)

#     if not cache.exists():
#         cache.mkdir()

#     config = home / "config.yaml"
#     if not config.exists():
#         github_token = input('Please enter your GitHub token: ')
#         config.open('w').write(
#             yaml.dump({
#                 "github_token": github_token
#             })
#         )
#         print("Saved GitHub token to {}".format(config))

#     config_data = yaml.safe_load(config.open())
#     config_data['cache'] = diskcache.Cache(cache)
#     return config_data



# if __name__ == "__main__":
#     main()