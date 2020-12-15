import sqlite3
import os
import sys
from shutil import copyfile
from typing import Optional
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
    except sqlite3.DatabaseError:
        logger.error(f'Invalid sqlite database: {dbfile!r}')
        sys.exit(1)

    copyfile(dbfile, DB)
    logger.info('database imported successfully')


def backup_db(name: Optional[str] = None) -> None:
    logger.info('backing up database')
    dest_filename = os.path.basename(DB)
    if name is not None:
        dest_filename = f'{name}.db'
    logger.info(f'copying database file to ./{dest_filename}')
    dest_filename = os.path.join(os.getcwd(), dest_filename)
    copyfile(DB, dest_filename)
