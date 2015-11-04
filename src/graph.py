class Graph:
    def __init__(self):
        self.edges = {}

    def add(self, vertex1, vertex2):
        vertex1 = vertex1.lower()
        vertex2 = vertex2.lower()

        if vertex1 not in self.edges:
            self.edges[vertex1] = [vertex2]
        elif vertex2 not in self.edges[vertex1]: 
                self.edges[vertex1].append(vertex2)

        if vertex2 not in self.edges:
            self.edges[vertex2] = [vertex1]
        elif vertex2 not in self.edges[vertex1]: 
            self.edges[vertex2].append(vertex1) 

    def remove(self, vertex1, vertex2):
        vertex1 = vertex1.lower()
        if vertex1 in self.edges:
            edgesacent_vertices = self.edges[vertex1]
            for vertex2 in edgesacent_vertices:
                try:
                    self.edges[vertex2].remove(vertex1)
                except ValueError:
                    pass
                except KeyError:
                    print "Key",vertex2,"is not found in:"
                    self.show()
            self.edges.pop(vertex1, None)
            
    def show(self):
        for vertex in self.edges:
            print "Vertex:",vertex,"-",self.edges[vertex]

