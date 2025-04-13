#!/bin/bash

set -e

echo "Waiting for PostgreSQL to start..."

#echo "Let the DB start"
python ./src/db_pre_start.py

echo "Applying database migrations..."
alembic upgrade head

#while ! python -c "
#import asyncio
#import os
#from asyncpg import connect
#
#async def check_db():
#    try:
#        conn = await connect(os.getenv('DB_URL'))
#        await conn.close()
#        return True
#    except:
#        return False
#
#asyncio.run(check_db())
#"; do
#  sleep 1
#done

echo "PostgreSQL started"

#alembic upgrade head

exec "$@"