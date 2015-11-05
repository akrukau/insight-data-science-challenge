from collections import Counter

class Graph:
    '''
    Class graph stores information about tweet connectivity.
    
    The class stores all edges and degrees of all vertices.
    For each edge, we also store in self.edges how many times this edge occur.
    However, when we count vertex degrees, we consider only whether two vertices
    are connected or not.

    Here is an example.
    Tweet 1: "#Apache #Spark" 13:00:01
    Tweet 2: "#Apache #Spark" 13:00:30
    Tweet 3: "#Apache #Hadoop" 13:01:25
    When Tweet 3 arrives, first tweet is deleted. However, the tags
    #Apache and #Spark still remain connected because of the second tweet.
    Therefore, after the second tweet, we store in self.edges that 
    #Apache and #Spark are connected with two edges. However, when
    we calculate vertex degrees, we assume there is only 
    one edge between #Apache and #Spark.

    We also store number of vertices with degree more than zero and 
    sum of vertex degrees.
    We update these variables when we add or remove edges. 
    This is more efficient than summing all the degrees at every graph update.
    '''
    def __init__(self):
        self.edges = Counter()
        self.degrees = Counter()
        self.sum_degrees = 0
        self.number_vertices = 0

    def add_edges(self, tags):
        '''Add edges between each pair of tags'''
        # Input tags are all in lowercase ascii characters.
        if (len(tags) >= 2):
            pairs_tags = [(i, j) for i in tags for j in tags if i != j]
            for (i, j) in pairs_tags:
                self.edges[(i, j)] += 1
                if self.edges[(i, j)] == 1:
                    self.sum_degrees += 1
                    self.degrees[i] += 1
                    if self.degrees[i] == 1:
                        self.number_vertices += 1

    def remove_edges(self, tags):
        '''Remove edges between each pair of tags'''
        # Input tags are all in lowercase ascii characters.
        if (len(tags) >= 2):
            pairs_tags = [(i, j) for i in tags for j in tags if i != j]
            for (i, j) in pairs_tags:
                self.edges[(i, j)] -= 1
                if self.edges[(i, j)] == 0:
                    self.sum_degrees -= 1
                    self.degrees[i] -= 1
                    if self.degrees[i] == 0:
                        self.number_vertices -= 1

    def show_edges(self):
        '''Print all graph edges. For each edge, show how many time it occurs'''
        print "Graph", self.edges    
    
    def show_degrees(self):
        '''Print degrees of all graph vertices'''
        for vertex in self.degrees:
            print "Vertex", vertex, "degree", self.degrees[vertex]

    def average_degree(self):
        '''Show average degree of all vertices with at least one edge'''
        if self.number_vertices > 0:
            average_degree = 1.0 * self.sum_degrees / self.number_vertices
        else:    
            average_degree = 0.0
        info_average_degree = "{0:.2f}".format(average_degree)    
        print info_average_degree
        return average_degree

    def dump(self):
        '''Show detailed debugging information'''
        self.show_edges()
        self.show_degrees()
        self.average_degree()


