import htmlentitydefs
import re, string

# this pattern matches substrings of reserved and non-ASCII characters
pattern = re.compile(r"[\x80-\xff]+")

# create character map
entity_map = {}

for i in range(256):
    entity_map[chr(i)] = "&%d;" % i
    
for entity, char in htmlentitydefs.entitydefs.items():
        if entity_map.has_key(char):
            entity_map[char] = "&%s;" % entity

def _escape_entity(m, get=entity_map.get):
    return string.join(map(get, m.group()), "")

def escape(string):
    return pattern.sub(_escape_entity, string)

                                
