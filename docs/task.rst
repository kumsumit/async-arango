Tasks
-----

ArangoDB can schedule user-defined Javascript snippets as one-time or periodic
(re-scheduled after each execution) tasks. Tasks are executed in the context of
the database they are defined in.

**Example:**

.. testcode::

    from aioarango import ArangoClient

    # Initialize the ArangoDB client.
    client = ArangoClient()

    # Connect to "test" database as root user.
    db = await client.db('test', username='root', password='passwd')

    # List all active tasks
    await db.tasks()

    # Create a new task which simply prints parameters.
    await db.create_task(
        name='test_task',
        command='''
            var task = function(params){
                var db = require('@arangodb');
                db.print(params);
            }
            task(params);
        ''',
        params={'foo': 'bar'},
        offset=300,
        period=10,
        task_id='001'
    )

    # Retrieve details on a task by ID.
    await db.task('001')

    # Delete an existing task by ID.
    await db.delete_task('001', ignore_missing=True)

.. note::
    When deleting a database, any tasks that were initialized under its context
    remain active. It is therefore advisable to delete any running tasks before
    deleting the database.

Refer to :ref:`StandardDatabase` class for API specification.
