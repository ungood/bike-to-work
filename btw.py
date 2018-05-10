#!/usr/bin/env python

from collections import namedtuple
import networkx as nx
from networkx.algorithms.simple_paths import all_simple_paths
from networkx.drawing.nx_pydot import to_pydot

Route = namedtuple('Route', ['start', 'end', 'via', 'distance'])

graph = nx.MultiDiGraph()

class RouteTypes:
    ROAD = ('Road', 'red')
    MULTI_USE = ('Multi-use Trail', 'green')
    SHARROW = ('Sharrow', 'orange')
    GREENWAY = ('Greenway', 'orange')
    MAJOR_SEP = ('Road, Major Separation', 'yellow')
    MINOR_SEP = ('Road, Minor Separation', 'yellow')
    

def node(name, color):
    graph.add_node(name, color=color)
    
def point_node(name):
    graph.add_node()

def route(start, end, via, distance, route_type):
    distance = float(distance)
    graph.add_edge(start, end,
        via=via,
        weight=distance,
        route_type=route_type[0],
        color=route_type[1],
        label='{0}\n{1:0.1f}'.format(via, distance))
    
graph.add_node('Home', color='green')
for bridge in ['Ballard Locks', 'Ballard Bridge', 'Fremont Bridge', 'University Bridge', 'Montlake Bridge']:
    graph.add_node(bridge, color='blue')
for point in ["Fisherman's Terminal", 'Ballmer Yard', 'Diamond Marina', 'Fred Meyer']:
    graph.add_node(point, shape='point')
graph.add_node('Work', color='red')

route('Home', 'Golden Gardens', 'Golden Gardens Dr', 1.7, RouteTypes.ROAD)
route('Golden Gardens', 'Ballard Locks', 'B-G Trail', 1.9, RouteTypes.MULTI_USE)
route('Home', 'Ballard Locks', '32nd Ave', 2, RouteTypes.SHARROW)
route('Home', 'Ballard Locks', '28th Ave', 1.7, RouteTypes.ROAD)
route('Ballard Locks', "Fisherman's Terminal", 'Commodore Way', 1.1, RouteTypes.ROAD)
route("Fisherman's Terminal", 'Ballmer Yard', 'Gilman Ave', 1.1, RouteTypes.MAJOR_SEP)
route('Ballmer Yard', 'Myrtle Edwards', 'Elliot Bay Trail', 2.1, RouteTypes.MULTI_USE)
route('Myrtle Edwards', 'Work', 'Mercer St', 1.6, RouteTypes.ROAD)
route('Myrtle Edwards', 'Work', 'Broad St', 1.5, RouteTypes.ROAD)
route("Fisherman's Terminal", 'Diamond Marina', 'Ship Canal Trail', 2.3, RouteTypes.MULTI_USE)
route('Diamond Marina', 'Lake Union Park', 'Lake Union Loop', 1.5, RouteTypes.MULTI_USE)
route('Lake Union Park', 'Work', 'Terry Ave', 0.4, RouteTypes.ROAD)

route('Home', 'Ballard Bridge', '24th Ave', 2.5, RouteTypes.MINOR_SEP)
route('Home', 'Ballard Bridge', '17th Ave', 2.6, RouteTypes.SHARROW)
route('Ballard Bridge', 'Diamond Marina', 'Ship Canal Trail', 2.6, RouteTypes.MULTI_USE)
route('Ballard Bridge', 'Myrtle Edwards', 'Elliot Bay Trail', 3.5, RouteTypes.MULTI_USE)

route('Home', 'Fred Meyer', '24th Ave', 2.9, RouteTypes.MINOR_SEP)
route('Home', 'Fred Meyer', '17th Ave', 3.2, RouteTypes.SHARROW)
route('Home', 'Fred Meyer', '8th Ave', 3.2, RouteTypes.MINOR_SEP)

route('Fred Meyer', 'Fremont Bridge', 'B-G Trail', 1.2, RouteTypes.MULTI_USE)
route('Fremont Bridge', 'Diamond Marina', '-', 0.3, RouteTypes.MULTI_USE)
route('Fremont Bridge', 'Work', 'Dexter Ave', 2.4, RouteTypes.MINOR_SEP)

route('Fred Meyer', 'University Bridge', 'B-G Trail', 3.2, RouteTypes.MULTI_USE)
route('University Bridge', 'Lake Union Park', 'Eastlake Ave', 2.2, RouteTypes.MINOR_SEP)

route('Fred Meyer', 'Montlake Bridge', 'B-G Trail', 4.0, RouteTypes.MULTI_USE)
route('Montlake Bridge', 'Lake Union Park', 'Delmar Dr', 3.3, RouteTypes.MINOR_SEP)

route('Home', 'Greenlake', '77th St', 2.8, RouteTypes.ROAD)
route('Greenlake', 'University Bridge', 'Roosevelt Way', 2.9, RouteTypes.MINOR_SEP)
route('Greenlake', 'Fremont Bridge', 'Stone Way', 3.3, RouteTypes.MINOR_SEP)
 
num_paths = len(list(all_simple_paths(graph, 'Home', 'Work')))
print("Calculated {0} paths".format(num_paths))

def dfs(node, target, path=[]):
    if node == target:
        yield path
    for s, e, data in graph.edges(node, data=True):
        new_path = list(path)
        new_path.append((s, e, data))
        yield from dfs(e, target, new_path)

for path in dfs('Home', 'Work'):
     label = 'Home'
     distance = 0.
     for s, e, data in path:
         label += ' -> ' + data['via'] + ' -> ' + e
         distance += data['weight']
     print('{0:0.2f}\t{1}'.format(distance, label))

gv = to_pydot(graph)
gv.write('bike-to-work.dot')
gv.write_png('bike-to-work.png', prog='dot')

