# want to count and find the edges within stackoverflow subgraphs

from collections import defaultdict
import xml.sax


class PostHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""
        self.Id = ""
        self.parentId = ""
        self.body = ""
        sid_set = set()
        with open('all_sid_parent_edges.txt') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().split(" ")
                sid1, sid2 = line[0], line[1]
                sid_set.add(sid1)
                sid_set.add(sid2)

        subgraphs = defaultdict(set)
        with open('all_sid_link_edges.txt') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().split(" ")
                sid1 = line[0]
                sid2 = line[1]
                if sid1 in sid_set:
                    subgraphs[sid1].add(sid2)
                if sid2 in sid_set:
                    subgraphs[sid2].add(sid1)
        # record the subgraphs
        self.subgraphs = subgraphs
       
        # total number of posts parsed
        self.count = 0
        # all post links, format: (sid1(original), sid2, type(1->linked or 3->duplicate))
        self.newEdges = set()


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
            for subgraph in self.subgraphs.values():
                if Id in subgraph and linkedId in subgraph:
                    # record new edge
                    edge = (Id, linkedId, linkType)
                    self.newEdges.add(edge)
                
            

    # Call when an elements ends
    def endElement(self, tag):
        self.CurrentData = ""
        self.Id = ""
        self.parentId = ""
        self.body = ""


    def getNewEdges(self):
        return self.newEdges
   

 
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
      

    newEdges = Handler.getNewEdges()
    # write new edges to a txt file
    with open('all_subgraph_edges.txt', 'a+') as f:
        for sid, sid_l, type in newEdges:
            line = sid + " " + sid_l + " " + type + "\n"
            f.write(line)



