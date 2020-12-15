import sqlite3
import os
import sys
from shutil import copyfile
from course_manager.logger import get_logger
from course_manager.db import DB

logger = get_logger(__name__)


def import_db(dbfile: str) -> None:
    logger.info(f'importing database {dbfile!r}')
    if not os.path.exists(dbfile):
        logger.error(f'File {dbfile!r} does not exist')
        sys.exit(1)
    try:
        with sqlite3.connect(dbfile) as conn:
            conn.execute(
                'SELECT course_id, timestamp, name, current_task, '
                'next_task FROM course'
            )
    except sqlite3.DatabaseError as exc:
        logger.error(f'Invalid sqlite database: {dbfile!r}')
        sys.exit(1)

    copyfile(dbfile, DB)
    logger.info('database imported successfully')
