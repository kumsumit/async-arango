Server Administration
---------------------

aioarango provides operations for server administration and monitoring.
Most of these operations can only be performed by admin users via ``_system``
database.

**Example:**

.. testcode::

    from aioarango import ArangoClient

    # Initialize the ArangoDB client.
    client = ArangoClient()

    # Connect to "_system" database as root user.
    sys_db = await client.db('_system', username='root', password='passwd')

    # Retrieve the server version.
    await sys_db.version()

    # Retrieve the server details.
    await sys_db.details()

    # Retrieve the target DB version.
    await sys_db.required_db_version()

    # Retrieve the database engine.
    await sys_db.engine()

    # Retrieve the server time.
    await sys_db.time()

    # Retrieve the server role in a cluster.
    await sys_db.role()

    # Retrieve the server statistics.
    await sys_db.statistics()

    # Read the server log.
    await sys_db.read_log(level="debug")

    # Retrieve the log levels.
    await sys_db.log_levels()

    # Set the log .
    await sys_db.set_log_levels(
        agency='DEBUG',
        collector='INFO',
        threads='WARNING'
    )

    # Echo the last request.
    await sys_db.echo()

    # Reload the routing collection.
    await sys_db.reload_routing()

    # Retrieve server metrics.
    await sys_db.metrics()


Features available in enterprise edition only:

.. code-block:: python

    from aioarango import ArangoClient

    # Initialize the ArangoDB client.
    client = ArangoClient()

    # Connect to "_system" database as root user using JWT authentication.
    sys_db = await client.db(
        '_system',
        username='root',
        password='passwd',
        auth_method='jwt'
    )

    # Retrieve JWT secrets.
    await sys_db.jwt_secrets()

    # Hot-reload JWT secrets.
    await sys_db.reload_jwt_secrets()

    # Rotate the user-supplied keys for encryption.
    await sys_db.encryption()


See :ref:`StandardDatabase` for API specification.
