# script that find all stackoverflow post that contains a github link

import xml.sax
import re
import json

total_posts = 2

def find_all_github_link(post, id):
    # .+ is one or more any character except newline
    # [^"] exluces the case "https://github.com/" (main page), 
    # but potentially can have ['https://github.com/ or <a href="http://example.com/https://github.com/']

    matches = re.findall('https://github\.com/[^"].+ rel', post)
    if len(matches)==0:
        return None 
    # print("ALL MATCHES: ")
    # print(matches)
    links = []
    for match in matches:
        index = match.find("rel")
        # remove ", space, and all after rel
        link = match[0:index-2]
        link_id = {"link":link, "id" : id}
        links.append(link_id)
    # print("LINKS: ")
    # print(links)
    return links

class PostHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""
        self.Id = ""
        self.parentId = ""
        self.body = ""
        # total number of posts parsed
        self.count = 0
        # group original post and its replies together where key is parent id and value is a list of reply id
        self.group = {}
        # all github related links found
        self.allLinks = []

        # all posts that contain a github link
        self.allPosts = []


        # read in target ids
        self.idSet = set()
        with open('../no_dup_links.json') as f:
            data = json.load(f)
            for entry in data:
                self.idSet.add(entry['id'])


    # Call when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "row":
            self.body = attributes['Body']
            self.Id = str(attributes['Id'])
                
            if self.Id in self.idSet:
                # add post information to allPosts
                post = {}
                for attribute in attributes.getNames():
                    post[attribute] = attributes[attribute]
                self.allPosts.append(post)
            



            #links = find_all_github_link(self.body,self.Id) 
           # if links:
            #    self.count += 1
             #   self.allLinks.extend(links)
                
                # add post information to allPosts 
              #  post = {}
               # for attribute in attributes.getNames():
                #    post[attribute] = attributes[attribute]
                #self.allPosts.append(post)



                # print(self.Id)
                # group question posts with posts replies
                # postTypeId = attributes['PostTypeId']
                # if postTypeId == '2':
                #     self.parentId = str(attributes['ParentId'])
                #     if self.parentId not in self.group:
                #         self.group[self.parentId] = []
                #     self.group[self.parentId].append(self.Id)

                # # specific case
                # if self.Id == '151005' or self.Id == '935392' or self.parentId == '151005':
                #     print(self.body)


            

    # Call when an elements ends
    def endElement(self, tag):
        self.CurrentData = ""
        self.Id = ""
        self.parentId = ""
        self.body = ""

        
        # abandon parsing after 30,000 posts
        #if self.count >= total_posts:
        #    raise xml.sax.SAXException('End of posts')

    def getLinks(self):
        return self.allLinks

    def getGroup(self):
        return self.group

    def getPosts(self):
        return self.allPosts
   


if ( __name__ == "__main__"):
    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    # override the default ContextHandler
    Handler = PostHandler()
    parser.setContentHandler( Handler )
    try:
        parser.parse("../Posts.xml")
    # end after parsing total_posts
    except xml.sax.SAXException as e:
        print(e)
        print("finished parsing " + str(total_posts))
        # find the largest group
        # maxx = 0
        # max_p = ""
        # max_r = []
        # for parent, replies in group.items():
        #     if len(replies)>maxx:
        #         maxx = len(replies)
        #         max_p = parent
        #         max_r = replies

    # links = Handler.getLinks()
    # group = Handler.getGroup()

    # wrote into a json file
    # with open("new_extracted_links.json","a") as f:
    #    json.dump(links,f)

    posts = Handler.getPosts()
    with open("posts1.json","a") as f:
        json.dump(posts,f, indent=4)
