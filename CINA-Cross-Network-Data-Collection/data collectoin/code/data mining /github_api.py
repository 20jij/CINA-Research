import requests
import json
import time 
import timeout_decorator 


class GitHub_API():
    # default is my own github access token
    def __init__(self,  proxy=None, username="20jij", token="") -> None:
        self.username = username
        self.token = token
        self.proxy = proxy

    # if it takes too long to request, there may be hundreds of thousands of related repos and we will skip it
    @timeout_decorator.timeout(600)
    def find_forks(self, author, repo_name):
        try:
            links = []
            page = 1
            while 1:
                url = "https://api.github.com/repos/" + author + "/" + repo_name + "/forks?per_page=100&page=" + str(page)
                response = requests.get(url, auth =(self.username, self.token), proxies=self.proxy)
                status = response.status_code

                # CHECK STATUS CODE: 200: success, 403: rate limit exceed, 404: invalid url
                # if rate limit exceeds, wait for 30 min
                if status == 403:
                    print(self.proxy)
                    time.sleep(900)
                    # skip the rest and request the same page again
                    continue

                # if invalid url, raise exception
                elif status == 404:
                    raise Exception("Invalid url" + url)

                # if success response
                elif response.status_code == 200:
                    data = response.json()
                    for entry in data:
                        link = entry['html_url']
                        links.append(link)
                    page+=1
                    # break if this is the last page
                    if len(data)<100:
                        break
                    
            return links
        # if there is exception for invalid url (or other unknown exception), return None
        except Exception as e:
            print(e)
            return None


    @timeout_decorator.timeout(600)
    def find_watchers(self, author, repo_name):
        try:
            links = []
            page = 1
            while 1:
                url = "https://api.github.com/repos/" + author + "/" + repo_name + "/subscribers?per_page=100&page=" + str(page)
                response = requests.get(url, auth =(self.username, self.token), proxies=self.proxy)
                status = response.status_code
                
                # CHECK STATUS CODE: 200: success, 403: rate limit exceed, 404: invalid url
                # if rate limit exceeds, wait for an hour
                if status == 403:
                    print(self.proxy)
                    time.sleep(900)
                    # skip the rest and request the same page again
                    continue

                # if invalid url, raise exception
                elif status == 404:
                    raise Exception("Invalid url" + url)

                # if success response
                elif response.status_code == 200:
                    data = response.json()
                    for entry in data:
                        link = entry['html_url']
                        links.append(link)
                    page+=1
                    # break if this is the last page
                    if len(data)<100:
                        break
                    
            return links
        # if there is exception for invalid url (or other unknown exception), return None
        except Exception as e:
            print(e)
            return None

    @timeout_decorator.timeout(600)
    def find_stargazers(self, author, repo_name):
        try:
            links = []
            page = 1
            while 1:
                url = "https://api.github.com/repos/" + author + "/" + repo_name + "/stargazers?per_page=100&page=" + str(page)
                response = requests.get(url, auth =(self.username, self.token), proxies=self.proxy)
                status = response.status_code

                # CHECK STATUS CODE: 200: success, 403: rate limit exceed, 404: invalid url
                # if rate limit exceeds, wait for an hour
                if status == 403:
                    print(self.proxy)
                    time.sleep(900)
                    # skip the rest and request the same page again
                    continue

                # if invalid url, raise exception
                elif status == 404:
                    raise Exception("Invalid url" + url)

                # if success response
                elif response.status_code == 200:
                    data = response.json()
                    for entry in data:
                        link = entry['html_url']
                        links.append(link)
                    page+=1
                    # break if this is the last page
                    if len(data)<100:
                        break
                    
            return links
        # if there is exception for invalid url, return None
        except Exception as e:
            print(e)
            return None
        

    @timeout_decorator.timeout(600) 
    def find_contributors(self, author, repo_name):
        try:
            links = []
            page = 1
            while 1:
                url = "https://api.github.com/repos/" + author + "/" + repo_name + "/contributors?per_page=100&page=" + str(page)
                response = requests.get(url, auth =(self.username, self.token), proxies=self.proxy)
                status = response.status_code

                # CHECK STATUS CODE: 200: success, 403: rate limit exceed, 404: invalid url
                # if rate limit exceeds, wait for an hour
                if status == 403:
                    print(self.proxy)
                    time.sleep(900)
                    # skip the rest and request the same page again
                    continue

                # if invalid url, raise exception
                elif status == 404:
                    raise Exception("Invalid url" + url)

                # if success response
                elif response.status_code == 200:
                    data = response.json()
                    for entry in data:
                        link = entry['html_url']
                        links.append(link)
                    page+=1
                    # break if this is the last page
                    if len(data)<100:
                        break
                    
            return links
        # if there is exception for invalid url, return None
        except Exception as e:
            print(e)
            return None




    def code_scanning(self, author, repo_name):
        try:
            links = []
            page = 1
            url = "https://api.github.com/repos/" + author + "/" + repo_name + "/code-scanning/alerts?per_page=100&page=" + str(page)
            response = requests.get(url, auth =(self.username, self.token), proxies=self.proxy)
            status = response.status_code
            # print(response.text)
            # if invalid url, raise exception
            if status == 404:
                raise Exception("Invalid url" + url)

            # if success response
            elif response.status_code == 200:
                data = response.json()
                print(data)
                return True
            
            # while 1:
            #     url = "https://api.github.com/repos/" + author + "/" + repo_name + "/code-scanning/alerts?per_page=100&page=" + str(page)
            #     response = requests.get(url, auth =(username, token))
            #     status = response.status_code

            #     # CHECK STATUS CODE: 200: success, 403: rate limit exceed, 404: invalid url
            #     # if rate limit exceeds, wait for an hour
            #     if status == 403:
            #         time.sleep(900)
            #         # skip the rest and request the same page again
            #         continue

            #     # if invalid url, raise exception
            #     elif status == 404:
            #         raise Exception("Invalid url" + url)

            #     # if success response
            #     elif response.status_code == 200:
            #         data = response.json()
            #         print(data)
            #         # for entry in data:
            #         #     link = entry['html_url']
            #         #     links.append(link)
            #         # page+=1
            #         # # break if this is the last page
            #         # if len(data)<100:
            #         #     break
                    
            return False
        # if there is exception for invalid url, return None
        except Exception as e:
            # print(e)
            return False




# author = "ruckus"
# repo_name = "ruckusing-migrations"

# find_forks(author, repo_name)
# find_watchers(author, repo_name)
# find_stargazers(author, repo_name)
# # find_contributors(author, repo_name)
# code_scanning(author, repo_name)




