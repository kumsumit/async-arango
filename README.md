![Logo](https://user-images.githubusercontent.com/9555251/124462469-5ecb0e80-dd9a-11eb-9083-01f3e827f8d1.png)

[![CodeCov](https://codecov.io/gh/mirrorrim/aioarango/branch/main/graph/badge.svg?token=DXg0O4hxnx)](https://codecov.io/gh/mirrorrim/aioarango)
[![PyPI version](https://badge.fury.io/py/aioarango.svg)](https://badge.fury.io/py/aioarango)
[![GitHub license](https://img.shields.io/badge/license-MIT-brightgreen)](https://github.com/mirrorrim/aioarango/blob/main/LICENSE)
![Python version](https://img.shields.io/badge/python-3.7%2B-blue)

# aioarango

Asynchronous python driver for [ArangoDB](https://www.arangodb.com), a scalable multi-model
database natively supporting documents, graphs and search.

This project is forked from [python-arango](https://github.com/joowani/python-arango). 
The only change is support for asynchronous API including tests. 
The current version (1.0.0) fully corresponds to python-arango 7.2.0.

## Requirements

- ArangoDB version 3.7+
- Python version 3.7+

## Installation

```shell
pip install aioarango
```

## Getting Started

Here is a simple usage example:

```python
from aioarango import ArangoClient

# Initialize the client for ArangoDB.
client = ArangoClient(hosts="http://localhost:8529")

# Connect to "_system" database as root user.
sys_db = await client.db("_system", username="root", password="passwd")

# Create a new database named "test".
await sys_db.create_database("test")

# Connect to "test" database as root user.
db = await client.db("test", username="root", password="passwd")

# Create a new collection named "students".
students = await db.create_collection("students")

# Add a hash index to the collection.
await students.add_hash_index(fields=["name"], unique=True)

# Insert new documents into the collection.
await students.insert({"name": "jane", "age": 39})
await students.insert({"name": "josh", "age": 18})
await students.insert({"name": "judy", "age": 21})

# Execute an AQL query and iterate through the result cursor.
cursor = await db.aql.execute("FOR doc IN students RETURN doc")
student_names = [document["name"] async for document in cursor]
```

Another example with [graphs](https://www.arangodb.com/docs/stable/graphs.html):

```python
from aioarango import ArangoClient

# Initialize the client for ArangoDB.
client = ArangoClient(hosts="http://localhost:8529")

# Connect to "test" database as root user.
db = await client.db("test", username="root", password="passwd")

# Create a new graph named "school".
graph = await db.create_graph("school")

# Create vertex collections for the graph.
students = await graph.create_vertex_collection("students")
lectures = await graph.create_vertex_collection("lectures")

# Create an edge definition (relation) for the graph.
edges = await graph.create_edge_definition(
    edge_collection="register",
    from_vertex_collections=["students"],
    to_vertex_collections=["lectures"]
)

# Insert vertex documents into "students" (from) vertex collection.
await students.insert({"_key": "01", "full_name": "Anna Smith"})
await students.insert({"_key": "02", "full_name": "Jake Clark"})
await students.insert({"_key": "03", "full_name": "Lisa Jones"})

# Insert vertex documents into "lectures" (to) vertex collection.
await lectures.insert({"_key": "MAT101", "title": "Calculus"})
await lectures.insert({"_key": "STA101", "title": "Statistics"})
await lectures.insert({"_key": "CSC101", "title": "Algorithms"})

# Insert edge documents into "register" edge collection.
await edges.insert({"_from": "students/01", "_to": "lectures/MAT101"})
await edges.insert({"_from": "students/01", "_to": "lectures/STA101"})
await edges.insert({"_from": "students/01", "_to": "lectures/CSC101"})
await edges.insert({"_from": "students/02", "_to": "lectures/MAT101"})
await edges.insert({"_from": "students/02", "_to": "lectures/STA101"})
await edges.insert({"_from": "students/03", "_to": "lectures/CSC101"})

# Traverse the graph in outbound direction, breadth-first.
result = await graph.traverse(
    start_vertex="students/01",
    direction="outbound",
    strategy="breadthfirst"
)
```

Please see the [documentation](https://aioarango.readthedocs.io) for more details.
