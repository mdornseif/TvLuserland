# $Id: opml_parser.py,v 1.1 2002/11/03 21:24:59 drt Exp $
# simple OMPL channel parser

import xmllib

class ParseError(Exception):
    pass

class opml_parser(xmllib.XMLParser):

    def __init__(self):
        xmllib.XMLParser.__init__(self)
        self.channels = []

    def start_opml(self, attr):
        if attr.get("version") != "1.0":
            raise ParseError("unknown OPML version")

    def start_outline(self, attr):
        channel = attr.get("xmlUrl") or attr.get("xmlurl")
        if channel:
            self.add_channel(attr.get("title"), channel)

    def add_channel(self, title, channel):
        # can be overridden
        self.channels.append((title, channel))


def load(file):

    file = open(file)

    parser = opml_parser()
    parser.feed(file.read())
    parser.close()

    return parser.channels


if __name__ == "__main__":

    for title, channel in load("channels.opml"):
        print channel
