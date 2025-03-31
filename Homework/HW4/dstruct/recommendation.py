"""
Author: Nick Usich
File: recommendation.py
Purpose: Use propertygraph.py to make a simple book recommendation system
OUTPUT:

Book Graph:
Emily (Person)
	Knows: Spencer (Person)
	Bought: Database Design (Book)
Spencer (Person)
	Knows: Emily (Person)
	Knows: Brendan (Person)
	Bought: Database Design (Book)
	Bought: Cosmos (Book)
Database Design (Book)
Brendan (Person)
	Bought: Database Design (Book)
	Bought: DNA & You (Book)
Cosmos (Book)
DNA & You (Book)
Trevor (Person)
	Bought: Cosmos (Book)
	Bought: Database Design (Book)
Paxtyn (Person)
	Bought: Database Design (Book)
	Bought: The Life of Cronkite (Book)
The Life of Cronkite (Book)



Subgraph:
DNA & You (Book)
Spencer (Person)



Recommendation Property Graph:
DNA & You (Book)
Spencer (Person)
	Recommend: DNA & You (Book)
"""



from propertygraph import Node, Relationship, PropertyGraph


def books_to_recommend(graph, person):
    """Returns a list of books that the person's friends own, and they don't own already"""

    # Get the people who the person knows
    adjacent_people = graph.adjacent(node = person, node_category='Person')

    # Initialize a list to append into
    person_potential_books = []

    # Loop through people in the set of adjacent nodes of person category
    for p in adjacent_people:
        book_set = graph.adjacent(p, 'Book')
        # Loop through the set of nodes that are of book category
        for book in book_set:
            # Add the book if the person who is getting the recomendation doesn't already have it
            if book not in graph.adjacent(person, 'Book'):
                person_potential_books.append(book)
            else:
                continue
    return person_potential_books

def subgraph_recommended(graph, list_of_books, person):
    """ Converts a list of books into a property graph for recommendations"""
    sub1 = graph.subgraph(set(list_of_books))
    sub1.add_node(person)
    sub = graph.subgraph(set(list_of_books))
    sub.add_node(person)
    r = Relationship('Recommend')
    for book in list_of_books:
        sub.add_relationship(person, book, r)
    return sub, sub1

def main():
    # Initializing
    book_graph = PropertyGraph()
    emily = Node('Emily', 'Person')
    spencer = Node('Spencer', 'Person')
    brendan = Node('Brendan', 'Person')
    trevor = Node('Trevor', 'Person')
    paxtyn = Node('Paxtyn', 'Person')

    cosmos = Node('Cosmos', 'Book', {'Price': 17.00})
    database = Node('Database Design', 'Book', {'Price': 195.00})
    cronkite = Node('The Life of Cronkite', 'Book', {'Price': 29.95})
    dna = Node('DNA & You', 'Book', {'Price': 11.50})

    b = Relationship('Bought')
    k = Relationship('Knows')

    book_graph.add_relationship(emily, spencer, k)
    book_graph.add_relationship(emily, database, b)
    book_graph.add_relationship(spencer, emily, k)
    book_graph.add_relationship(spencer, brendan, k)
    book_graph.add_relationship(spencer, database, b)
    book_graph.add_relationship(spencer, cosmos, b)
    book_graph.add_relationship(brendan, database, b)
    book_graph.add_relationship(brendan, dna, b)
    book_graph.add_relationship(trevor, cosmos, b)
    book_graph.add_relationship(trevor, database, b)
    book_graph.add_relationship(paxtyn, database, b)
    book_graph.add_relationship(paxtyn, cronkite, b)

    # Printing results and using the functions from above

    books = books_to_recommend(book_graph, spencer)
    sub, sub1 = subgraph_recommended(book_graph, books, spencer)
    print(f'Book Graph:\n{book_graph}\n\n')
    print(f'Subgraph:\n{sub1}\n\n')
    print(f'Recommendation Property Graph:\n{sub}\n\n')


if __name__ == '__main__':
    main()


