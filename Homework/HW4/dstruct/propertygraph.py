"""
File: propertygraph.py
Description: An implementation of a PropertyGraph consisting of
Node and Relationship objects.  Nodes and Relationships carry
properties.  Property graphs are used to represent connected knowledge.
"""

class Node:

    def __init__(self, name, category, props=None):
        """ Class constructor """
        self.name = name
        self.category = category
        self.props = props

    def __getitem__(self, key):
        """ Fetch a property from the node using []
         return None if property doesn't exist """
        try:
            return self.props[key]
        except Exception:
            return None

    def __setitem__(self, key, value):
        """ Set a node property with a specified value using [] """
        if self.props is not None:
            try:
                self.props[key] = value
            except Exception:
                "Incorrect Type for set item"
        else:
            try:
                self.props = {key: value}
            except Exception:
                "Incorrect Type for set item"

    def __eq__(self, other):
        """ Two nodes are equal if they have the same
        name and category irrespective of their properties """
        if type(other) != Node:
            raise Exception("Incorrect type")
        return self.name == other.name and self.category == other.category

    def __hash__(self):
        """ By making Nodes hashable we can now
        store them as keys in a dictionary! """
        return hash((self.category, self.name))

    def __repr__(self):
        """ Output the node as a string in the following format:
        name:category<tab>properties.
        Note: __repr__ is more versatile than __str__ """
        if self.props is not None:
            return f'{self.name}:{self.category}\t{self.props}'
        if self.props is None:
            return f'{self.name}:{self.category}'


class Relationship:

    def __init__(self, category, props=None):
        """ Class constructor """
        self.category = category
        self.props = props

    def __getitem__(self, key):
        """ Fetch a property from the node using []
         return None if property doesn't exist """
        if self.props is not None:
            try:
                return self.props[key]
            except KeyError:
                return None
        else:
            return None

    def __setitem__(self, key, value):
        """ Set a node property with a specified value using [] """
        if self.props is not None:
            try:
                self.props[key] = value
            except KeyError:
                "Incorrect Type for set item"
        else:
            try:
                self.props = {key: value}
            except Exception:
                "Incorrect Type for set item"

    def __repr__(self):
        """ Output the relationship as a string in the following format:
        :category<space>properties.
        Note: __repr__ is more versatile than __str__ """
        if self.props is not None:
            return f':{self.category} {self.props}'
        if self.props is None:
            return f':{self.category}'


class PropertyGraph:

    def __init__(self):
        """ Construct an empty property graph """
        self.pg = {}

    def add_node(self, node):
        """ Add a node to the property graph """
        if type(node) != Node:
            raise Exception("Type for add_node must be Node")
        if node in list(self.pg.keys()):
            raise Exception("Node already exists")

        self.pg[node] = [(),()]

    def add_relationship(self, src, targ, rel):
        """ Connect src and targ nodes via the specified directed relationship.
        If either src or targ nodes are not in the graph, add them.
        Note that there can be many relationships between two nodes! """
        if type(src) != Node or type(targ) != Node:
            raise Exception("Type for add relationship src and trg must be Node")
        if type(rel) != Relationship:
            raise Exception("Type for add relationship rel must be Relationship")

        # Graph = {src (Node): [(targ1, targ2, targ2),(Rel1, Rel2, Rel3)]}
        if src not in self.pg:
            self.add_node(src)
        if targ not in self.pg:
            self.add_node(targ)
        self.pg[src] = [(self.pg[src])[0] + (targ,), (self.pg[src])[1] + (rel,)]

    def get_nodes(self, name=None, category=None, key=None, value=None):
        """ Return the SET of nodes matching all the specified criteria.
        If the criterion is None it means that the particular criterion is ignored. """

        if name is not None and type(name) != str:
            raise Exception("Name must be a string")
        if category is not None and type(category) != str:
            raise Exception("Category must be a string")
        if key is not None and type(key) != str:
            raise Exception("Key must be a string")
        if value is not None and type(value) not in (int, float):
            raise Exception("Value must be a float/int")
        matching_nodes = []
        for node in self.pg.keys():
            match = True
            if (key is not None or value is not None) and node.props is None:
                match = False
            if name is not None and node.name != name:
                match = False
            if category is not None and node.category != category:
                match = False
            if type(node.props) == dict:
                if key is not None:
                    if value is not None:
                        if node.props.get(key) != value:
                            match = False
                        else:
                            if key not in node.props:
                                match = False
            if match is True:
                matching_nodes.append(node)
        return set(matching_nodes)

    def adjacent(self, node, node_category=None, rel_category=None):
        """ Return a set of all nodes that are adjacent to node.
        If specified include only adjacent nodes with the specified node_category.
        If specified include only adjacent nodes connected via relationships with
        the specified rel_category """
        if node not in self.pg.keys():
            raise Exception("Node not found")
        if type(node) != Node:
            raise Exception("Type for node must be Node")

        adj_nodes = []
        for n in self.pg.keys():
            targs = self.pg[n][0]
            rels = self.pg[n][1]
            if node in targs:
                index = targs.index(node)
                rel = rels[index]
                match_1 = True
                if rel_category is not None and rel_category != rel.category:
                    match_1 = False
                if node_category is not None and node_category != n.category:
                    match_1 = False
                if match_1 is True:
                    adj_nodes.append(n)

        targs = self.pg[node][0]
        rels = self.pg[node][1]
        for n,r in enumerate(targs):
            rel = rels[n]
            match = True
            if node_category is not None and node_category != r.category:
                match = False
            if rel_category is not None and rel_category != rel.category:
                match = False
            if match is True:
                adj_nodes.append(r)
        return set(adj_nodes)

    def subgraph(self, nodes):
        """ Return the subgraph as a PropertyGraph consisting of the specified
        set of nodes and all interconnecting relationships """
        if type(nodes) != set:
            raise Exception("Nodes must be a set")

        sub_pg = PropertyGraph()
        for node in nodes:
            sub_pg.add_node(node)

        for src in nodes:
            if src in self.pg.keys():
                for targ, rel in zip((self.pg[src])[0], (self.pg[src])[1]):
                    if targ in nodes:
                        sub_pg.add_relationship(src, targ, rel)
        return sub_pg

    def __repr__(self):
        """ A string representation of the property graph
        Properties are not displayed.

        Node
            Relationship Node
            Relationship Node
            .
            .
            etc.
        Node
            Relationship Node
            Relationship Node
            .
            .
            etc.
        .
        .
        etc.
        """

        output = ''
        for src in self.pg.keys():
            output += f'{src.name} ({src.category})\n'
            if self.pg[src][0]:
                for targ, rel in zip(self.pg[src][0], self.pg[src][1]):
                    output += f'\t{rel.category}: {targ.name} ({targ.category})\n'
        return output

def main():
    a = Node('Nick', 'Person')
    b = Node('Souren', 'Person')
    c = Node('Pride and Prejudice', 'Book', {'Price': 20})
    d = Node('Dune', 'Book', {'Price': 20})

    e = Relationship('Bought', {'Price': 19.45})
    f = Relationship('Knows')

    test_graph = PropertyGraph()
    test_graph.add_node(a)
    test_graph.add_node(b)
    test_graph.add_node(c)
    test_graph.add_node(d)

    test_graph.add_relationship(a, b, f)
    test_graph.add_relationship(a, d, e)
    test_graph.add_relationship(a, c, e)
    test_graph.add_relationship(b, d, e)

    abc = test_graph.subgraph({a, b, c})
    comp = PropertyGraph()
    comp.add_node(c)
    comp.add_node(a)
    comp.add_node(b)
    comp.add_relationship(a, c, e)
    comp.add_relationship(a, b, f)

    """
    tester = test_graph.subgraph({b, d})
    print(tester)
    expected1 = (
        "Dune (Book)\n"
        "Souren (Person)\n"
        "\tBought: Dune (Book)\n"
    )
    expected2 = (
        "Souren (Person)\n"
        "\tBought: Dune (Book)\n"
        "Dune (Book)\n"
    )
    print(tester.__repr__() == expected1 or expected2)
    """
    ra = repr(a)
    rd = repr(d)

    print(ra == "Nick:Person")
    print(rd == "Dune:Book\t{'Price': 20}")

if __name__ == '__main__':
    main()