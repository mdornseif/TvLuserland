import xmlrpclib
from pprint import pprint
import mx.DateTime.Parser
import cPickle

appkey = '484A4B4A4601C20CDC68F98631BABF76E288C642AE'

server = xmlrpclib.Server("http://localhost:5335")#, verbose=1)

problems = [239, 377, 815, 1097, 1103, 1104, 1111, 1120, 1137,
1140, 1472, 1476, 1497, 1498, 1521, 1526, 1527, 1540, 1552, 1570,
1573, 1576, 1582, 1586, 1591, 1610, 1649, 1657, 1660, 1662, 1665,
1673, 1678, 1680, 1687, 1699, 1701, 1702, 1708, 1709, 1712, 1713,
1714, 1715, 1728, 1734, 1740, 1749, 1750, 1759, 1760, 1761, 1770,
1806, 1857, 1861, 1865, 1876, 1879, 1880, 1881, 1884, 1890, 1899,
1920, 1924, 1927, 1934, 1953, 1954, 1957, 1958, 1968, 1969, 1976,
1977, 2003, 2004, 2005, 2006, 2007, 2008, 2017, 2018, 2023, 2024,
2025, 2026, 2041, 2043, 2056, 2063, 2067, 2081, 2084, 2086, 2090,
2101, 2111, 2117, 2119, 2124, 2131, 2137, 2138, 2141, 2144, 2145,
2148, 2151, 2163, 2168, 2177, 2178, 2179, 2180, 2181, 2182, 2199,
2204, 2206, 2225, 2227, 2228, 2233, 2243, 2244, 2254, 2256, 2262,
2263, 2278, 2287, 2292, 2302, 2306, 2312, 2322, 2323, 2324, 2338,
2342, 2343, 2350, 2353, 2356, 2357, 2360, 2361, 2366, 2375, 2380,
2381, 2382, 2388, 2394, 2398, 2401, 2403, 2405, 2406, 2409, 2411,
2417, 2421, 2424, 2437, 2439, 2449, 2450, 2469, 2470, 2473, 2474,
2475, 2489, 2496, 2500, 2520, 2521, 2526, 2538, 2542, 2548, 2549,
2557, 2559, 2561, 2563, 2564, 2565, 2566, 2579, 2580, 2581, 2582,
2583, 2584, 2585, 2591, 2592, 2596, 2597, 2600, 2602, 2605, 2613,
2616, 2623, 2624, 2625, 2626, 2627, 2628, 2632, 2633, 2635, 2645,
2657, 2685, 2693, 2694, 2695, 2696, 2697, 2698, 2699, 2700, 2705,
2715, 2725, 2730, 2733, 2743, 2757, 2758, 2777, 2784, 2785, 2786,
2802, 2806, 2821, 2901, 2902, 2954, 2972, 2995, 2996, 3017, 3018,
3050, 3051, 3052, 3053, 3128, 3129]

def deunicode(ustr):
    if type(ustr) != type('abc'):
        print "unicode attacks!"
    return ustr.encode('latin1', 'replace')


#for i in problems:
for i in range(2995, 3129):
    try:
        print i
        data = server.md.metaWeblog.getPost(i, 'md', 'felix23')
        del(data["postid"])
        data["categories"] = data.get("categories", {})
        for x in data["categories"].keys():
            data["categories"][x] = data["categories"][x].value
        if data["flNotOnHomePage"].value:
            data["flNotOnHomePage"] = 1
        data["date"] = mx.DateTime.Parser.DateTimeFromString(data['when'].value)
        if 'postingDate' in data:
            data["postingDate"] = mx.DateTime.Parser.DateTimeFromString(data['postingDate'].value)
        data["title"] = deunicode(data.get("title", "")) 
        data["text"] = deunicode(data.get("text", ""))
        data["link"] = deunicode(data.get("link", "")) 
        fp=open("db/weblog/items/%s.pickle" % data['guid'], 'w')
        cPickle.dump(data, fp)
        fp.close()
    except:
        print "!!!"
        problems.append(i)

    #pprint(data)
    
print problems
