import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint


OSMFILE = "/Users/mnsarma/xml/toronto_canada.osm"
street_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


roads_types = ["Street", "Avenue", "Boulevard", "Lane", "Road", "Parkway", "Drive"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd.": "Road",
            }


def audit_street_type(street_types, street_name):
    m = street_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in roads_types:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):

    # YOUR CODE HERE
    k = street_re.search(name)
    k = k.group()
    if not k:
        raise Exception(name)
    l = mapping[k]
    if not l:
        raise Exception(k)
    new_name = re.sub(k, l, name)
    
    return new_name


#def test():
#    st_types = audit(OSMFILE)
#    assert len(st_types) == 3
#    pprint.pprint(dict(st_types))
#
#    for st_type, ways in st_types.iteritems():
#        for name in ways:
#            better_name = update_name(name, mapping)
#            print name, "=>", better_name
#            if name == "West Lexington St.":
#                assert better_name == "West Lexington Street"
#            if name == "Baldwin Rd.":
#                assert better_name == "Baldwin Road"
#
#
#if __name__ == '__main__':
#    test()