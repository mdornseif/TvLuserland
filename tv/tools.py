# (d)escape form the effbot

import htmlentitydefs
import re, string

# this pattern matches substrings of reserved and non-ASCII characters
_escape_re = re.compile(r"[\x80-\xff]+")

# create character map
_entity_map = {}

for i in range(256):
    _entity_map[chr(i)] = "&%d;" % i
    
for entity, char in htmlentitydefs.entitydefs.items():
        if _entity_map.has_key(char):
            _entity_map[char] = "&%s;" % entity

def _escape_entity(m, get=_entity_map.get):
    return string.join(map(get, m.group()), "")

def escape(string):
    return _escape_re.sub(_escape_entity, string)


_descape_re = re.compile("&(\w+?);")

def _descape_entity(m, defs=htmlentitydefs.entitydefs):
    # callback: translate one entity to its ISO Latin value
    try:
        return defs[m.group(1)]
    except KeyError:
        return m.group(0) # use as is
    
def descape(string):
    return _descape_re.sub(_descape_entity, string)

                            
