# script that extracts linked parent/answer relationship from Post.xml

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
        with open('gid_sid.txt') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().split(' ')
                if line[1] != ' ':
                    self.sid_set.add(line[1])
        # total number of posts parsed
        self.count = 0
        # all post links, format: (sid1(original), sid2)
        self.postLinks = set()


    # Call when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "row":
            # Title has key error? 
            # if attributes['Title']:
            #     self.title = attributes['Title']
            # print(attributes.getNames())
            linkedId = None
            if attributes['PostTypeId'] == 1:
                linkedId = str(attributes['AcceptedAnswerId'])
            elif attributes['PostTypeId'] == 2:
                linkedId = str(attributes['ParentId'])
            Id = str(attributes['Id'])

            # add connection to postLinks
            if linkedId and (Id in self.sid_set or linkedId in self.sid_set):
                connection = tuple(sorted([Id, linkedId]))
                print(connection)
                self.postLinks.add(connection)
                self.count+=1
            if self.count%1000 == 0:
                print(self.count)
            # print(self.postLinks)
            
            

    # Call when an elements ends
    def endElement(self, tag):
        self.CurrentData = ""
        self.Id = ""
        self.parentId = ""
        self.body = ""


    def getPostLinks(self):
        return self.postLinks
   


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
      

    links = Handler.getPostLinks()
    # write post link adjacency list to a txt file
    with open('all_sid_parent_edges.txt', 'w') as f:
        for sid, sid_l in links:
            line = sid + " " + sid_l + "\n"
            f.write(line)




