from datetime import datetime

import pytest

from aioarango.aql import AQL
from aioarango.backup import Backup
from aioarango.cluster import Cluster
from aioarango.database import StandardDatabase
from aioarango.errno import (
    DATABASE_NOT_FOUND,
    DUPLICATE_NAME,
    FORBIDDEN,
    USE_SYSTEM_DATABASE,
)
from aioarango.exceptions import (
    DatabaseCreateError,
    DatabaseDeleteError,
    DatabaseListError,
    DatabasePropertiesError,
    ServerDetailsError,
    ServerEchoError,
    ServerEngineError,
    ServerLogLevelError,
    ServerLogLevelSetError,
    ServerMetricsError,
    ServerReadLogError,
    ServerReloadRoutingError,
    ServerRequiredDBVersionError,
    ServerRoleError,
    ServerStatisticsError,
    ServerStatusError,
    ServerTimeError,
    ServerVersionError,
)
from aioarango.foxx import Foxx
from aioarango.pregel import Pregel
from aioarango.replication import Replication
from aioarango.wal import WAL
from tests.helpers import assert_raises, generate_db_name

pytestmark = pytest.mark.asyncio


async def test_database_attributes(db: StandardDatabase, username):
    assert db.context in ["default", "async", "batch", "transaction"]
    assert db.username == username
    assert db.db_name == db.name
    assert db.name.startswith("test_database")
    assert db.conn is not None
    assert repr(db) == f"<StandardDatabase {db.name}>"

    assert isinstance(db.aql, AQL)
    assert isinstance(db.backup, Backup)
    assert isinstance(db.cluster, Cluster)
    assert isinstance(db.foxx, Foxx)
    assert isinstance(db.pregel, Pregel)
    assert isinstance(db.replication, Replication)
    assert isinstance(db.wal, WAL)


async def test_database_misc_methods(sys_db: StandardDatabase, db: StandardDatabase, bad_db: StandardDatabase):
    # Test get properties
    properties = await db.properties()
    assert "id" in properties
    assert "path" in properties
    assert properties["name"] == db.name
    assert properties["system"] is False

    # Test get properties with bad database
    with assert_raises(DatabasePropertiesError) as err:
        await bad_db.properties()
    assert err.value.error_code in {11, 1228}

    # Test get server version
    assert isinstance(await db.version(), str)

    # Test get server version with bad database
    with assert_raises(ServerVersionError) as err:
        await bad_db.version()
    assert err.value.error_code in {11, 1228}

    # Test get server details
    details = await db.details()
    assert "architecture" in details
    assert "server-version" in details

    # Test get server details with bad database
    with assert_raises(ServerDetailsError) as err:
        await bad_db.details()
    assert err.value.error_code in {11, 1228}

    # Test get server required database version
    version = await db.required_db_version()
    assert isinstance(version, str)

    # Test get server target version with bad database
    with assert_raises(ServerRequiredDBVersionError):
        await bad_db.required_db_version()

    # Test get server metrics
    metrics = await db.metrics()
    assert isinstance(metrics, str)

    # Test get server statistics with bad database
    with assert_raises(ServerMetricsError) as err:
        await bad_db.metrics()
    assert err.value.error_code in {11, 1228}

    # Test get server statistics
    statistics = await db.statistics(description=False)
    assert isinstance(statistics, dict)
    assert "time" in statistics
    assert "system" in statistics
    assert "server" in statistics

    # Test get server statistics with description
    description = await db.statistics(description=True)
    assert isinstance(description, dict)
    assert "figures" in description
    assert "groups" in description

    # Test get server statistics with bad database
    with assert_raises(ServerStatisticsError) as err:
        await bad_db.statistics()
    assert err.value.error_code in {11, 1228}

    # Test get server role
    assert await db.role() in {"SINGLE", "COORDINATOR", "PRIMARY", "SECONDARY", "UNDEFINED"}

    # Test get server role with bad database
    with assert_raises(ServerRoleError) as err:
        await bad_db.role()
    assert err.value.error_code in {11, 1228}

    # Test get server status
    status = await db.status()
    assert "host" in status
    assert "operation_mode" in status
    assert "server_info" in status
    assert "read_only" in status["server_info"]
    assert "write_ops_enabled" in status["server_info"]
    assert "version" in status

    # Test get status with bad database
    with assert_raises(ServerStatusError) as err:
        await bad_db.status()
    assert err.value.error_code in {11, 1228}

    # Test get server time
    assert isinstance(await db.time(), datetime)

    # Test get server time with bad database
    with assert_raises(ServerTimeError) as err:
        await bad_db.time()
    assert err.value.error_code in {11, 1228}

    # Test echo (get last request)
    last_request = await db.echo()
    assert "protocol" in last_request
    assert "user" in last_request
    assert "requestType" in last_request
    assert "rawRequestBody" in last_request

    # Test echo with bad database
    with assert_raises(ServerEchoError) as err:
        await bad_db.echo()
    assert err.value.error_code in {11, 1228}

    # Test read_log with default parameters
    log = await sys_db.read_log(upto="fatal")
    assert "lid" in log
    assert "level" in log
    assert "text" in log
    assert "total_amount" in log

    # Test read_log with specific parameters
    log = await sys_db.read_log(
        level="error",
        start=0,
        size=100000,
        offset=0,
        search="test",
        sort="desc",
    )
    assert "lid" in log
    assert "level" in log
    assert "text" in log
    assert "total_amount" in log

    # Test read_log with bad database
    with assert_raises(ServerReadLogError) as err:
        await bad_db.read_log()
    assert err.value.error_code in {11, 1228}

    # Test reload routing
    assert isinstance(await db.reload_routing(), bool)

    # Test reload routing with bad database
    with assert_raises(ServerReloadRoutingError) as err:
        await bad_db.reload_routing()
    assert err.value.error_code in {11, 1228}

    # Test get log levels
    assert isinstance(await sys_db.log_levels(), dict)

    # Test get log levels with bad database
    with assert_raises(ServerLogLevelError) as err:
        await bad_db.log_levels()
    assert err.value.error_code in {11, 1228}

    # Test set log levels
    new_levels = {"agency": "DEBUG", "collector": "INFO", "threads": "WARNING"}
    result = await sys_db.set_log_levels(**new_levels)
    for key, value in new_levels.items():
        assert result[key] == value
    for key, value in (await sys_db.log_levels()).items():
        assert result[key] == value

    # Test set log levels with bad database
    with assert_raises(ServerLogLevelSetError):
        await bad_db.set_log_levels(**new_levels)

    # Test get storage engine
    engine = await db.engine()
    assert engine["name"] in ["rocksdb"]
    assert "supports" in engine

    # Test get storage engine with bad database
    with assert_raises(ServerEngineError) as err:
        await bad_db.engine()
    assert err.value.error_code in {11, 1228}


async def test_database_management(db: StandardDatabase, sys_db: StandardDatabase, bad_db: StandardDatabase):
    # Test list databases
    result = await sys_db.databases()
    assert "_system" in result

    # Test list databases with bad database
    with assert_raises(DatabaseListError):
        await bad_db.databases()

    # Test create database
    db_name = generate_db_name()
    assert await sys_db.has_database(db_name) is False
    assert (
        await sys_db.create_database(
            name=db_name, replication_factor=1, write_concern=1, sharding="single"
        )
        is True
    )
    assert await sys_db.has_database(db_name) is True

    # Test list database with bad database
    with assert_raises(DatabaseListError) as err:
        await bad_db.has_database(db_name)
    assert err.value.error_code == FORBIDDEN

    # Test has database with bad database
    with assert_raises(DatabaseListError) as err:
        await bad_db.has_database(db_name)
    assert err.value.error_code == FORBIDDEN

    # Test create duplicate database
    with assert_raises(DatabaseCreateError) as err:
        await sys_db.create_database(db_name)
    assert err.value.error_code == DUPLICATE_NAME

    # Test create database without permissions
    with assert_raises(DatabaseCreateError) as err:
        await db.create_database(db_name)
    assert err.value.error_code == USE_SYSTEM_DATABASE

    # Test delete database without permissions
    with assert_raises(DatabaseDeleteError) as err:
        await db.delete_database(db_name)
    assert err.value.error_code == USE_SYSTEM_DATABASE

    # Test delete database
    assert await sys_db.delete_database(db_name) is True
    assert db_name not in await sys_db.databases()

    # Test delete missing database
    with assert_raises(DatabaseDeleteError) as err:
        await sys_db.delete_database(db_name)
    assert err.value.error_code in {FORBIDDEN, DATABASE_NOT_FOUND}
    assert await sys_db.delete_database(db_name, ignore_missing=True) is False
