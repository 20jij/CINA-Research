# script that extracts stack overflow attributes from Posts.xml

import sys
import xml.sax
import re
import json



class PostHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""
        self.Id = ""
        self.parentId = ""
        self.body = ""
        # record the target sid
        self.sid_set = set()
        with open('all_sid_parent_edges.txt') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().split(' ')
                self.sid_set.add(line[0])
                self.sid_set.add(line[1])
        with open('all_sid_link_edges.txt') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().split(" ")
                self.sid_set.add(line[0])
                self.sid_set.add(line[1])
        # total number of posts parsed
        self.count = 0
        self.allPosts = []


    # Call when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "row":
            self.body = attributes['Body']
            self.Id = str(attributes['Id'])
                
            if self.Id in self.sid_set:
                # add post information to allPosts
                post = {}
                for attribute in attributes.getNames():
                    post[attribute] = attributes[attribute]
                self.allPosts.append(post)
                self.count+=1
                if (self.count%10000) == 0:
                    print(self.count)
                
            

    # Call when an elements ends
    def endElement(self, tag):
        self.CurrentData = ""
        self.Id = ""
        self.parentId = ""
        self.body = ""


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
      
    posts = Handler.getPosts()
    with open("all_posts.json","w") as f:
        json.dump(posts,f, indent=4)





