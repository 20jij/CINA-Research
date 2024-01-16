# script that extracts linked Posts relationship from PostLinks.xml

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
        with open('gid_sid.txt') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().split(' ')
                if line[1] != ' ':
                    self.sid_set.add(line[1])
        # total number of posts parsed
        self.count = 0
        # all post links, format: (sid1(original), sid2, type(1->linked or 3->duplicate))
        self.postLinks = set()


    # Call when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "row":
            # Title has key error? 
            # if attributes['Title']:
            #     self.title = attributes['Title']
            # print(attributes.getNames())
            Id = str(attributes['PostId'])
            linkedId = str(attributes['RelatedPostId'])
            linkType = str(attributes['LinkTypeId'])
            if Id in self.sid_set or linkedId in self.sid_set:
                # add connection to postLinks
                connection = (Id, linkedId, linkType)
                self.postLinks.add(connection)
                self.count+=1
                if (self.count%10000) == 0:
                    print(self.count)
                
            

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
        parser.parse("../PostLinks.xml")
    # end after parsing total_posts
    except xml.sax.SAXException as e:
        print(e)
      

    links = Handler.getPostLinks()
    # write post link adjacency list to a txt file
    with open('all_sid_link_edges.txt', 'w') as f:
        for sid, sid_l, type in links:
            line = sid + " " + sid_l + " " + type + "\n"
            f.write(line)




