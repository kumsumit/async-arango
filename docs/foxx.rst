Foxx
----

aioarango provides support for **Foxx**, a microservice framework which
lets you define custom HTTP endpoints to extend ArangoDB's REST API. For more
information, refer to `ArangoDB manual`_.

.. _ArangoDB manual: https://docs.arangodb.com

**Example:**

.. testcode::

    from aioarango import ArangoClient

    # Initialize the ArangoDB client.
    client = ArangoClient()

    # Connect to "_system" database as root user.
    db = await client.db('_system', username='root', password='passwd')

    # Get the Foxx API wrapper.
    foxx = db.foxx

    # Define the test mount point.
    service_mount = '/test_mount'

    # List services.
    await foxx.services()

    # Create a service using source on server.
    await foxx.create_service(
        mount=service_mount,
        source='/tmp/service.zip',
        config={},
        dependencies={},
        development=True,
        setup=True,
        legacy=True
    )

    # Update (upgrade) a service.
    service = await db.foxx.update_service(
        mount=service_mount,
        source='/tmp/service.zip',
        config={},
        dependencies={},
        teardown=True,
        setup=True,
        legacy=False
    )

    # Replace (overwrite) a service.
    service = await db.foxx.replace_service(
        mount=service_mount,
        source='/tmp/service.zip',
        config={},
        dependencies={},
        teardown=True,
        setup=True,
        legacy=True,
        force=False
    )

    # Get service details.
    await foxx.service(service_mount)

    # Manage service configuration.
    await foxx.config(service_mount)
    await foxx.update_config(service_mount, config={})
    await foxx.replace_config(service_mount, config={})

    # Manage service dependencies.
    await foxx.dependencies(service_mount)
    await foxx.update_dependencies(service_mount, dependencies={})
    await foxx.replace_dependencies(service_mount, dependencies={})

    # Toggle development mode for a service.
    await foxx.enable_development(service_mount)
    await foxx.disable_development(service_mount)

    # Other miscellaneous functions.
    await foxx.readme(service_mount)
    await foxx.swagger(service_mount)
    await foxx.download(service_mount)
    await foxx.commit(service_mount)
    await foxx.scripts(service_mount)
    await foxx.run_script(service_mount, 'setup', [])
    await foxx.run_tests(service_mount, reporter='xunit', output_format='xml')

    # Delete a service.
    await foxx.delete_service(service_mount)

You can also manage Foxx services by using zip or Javascript files directly:

.. code-block:: python

    from aioarango import ArangoClient

    # Initialize the ArangoDB client.
    client = ArangoClient()

    # Connect to "_system" database as root user.
    db = await client.db('_system', username='root', password='passwd')

    # Get the Foxx API wrapper.
    foxx = db.foxx

    # Define the test mount point.
    service_mount = '/test_mount'

    # Create a service by providing a file directly.
    await foxx.create_service_with_file(
        mount=service_mount,
        filename='/home/user/service.zip',
        development=True,
        setup=True,
        legacy=True
    )

    # Update (upgrade) a service by providing a file directly.
    await foxx.update_service_with_file(
        mount=service_mount,
        filename='/home/user/service.zip',
        teardown=False,
        setup=True,
        legacy=True,
        force=False
    )

    # Replace a service by providing a file directly.
    await foxx.replace_service_with_file(
        mount=service_mount,
        filename='/home/user/service.zip',
        teardown=False,
        setup=True,
        legacy=True,
        force=False
    )

    # Delete a service.
    await foxx.delete_service(service_mount)

See :ref:`Foxx` for API specification.
