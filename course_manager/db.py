import sqlite3
from pathlib import Path
from course_manager.logger import get_logger
from typing import Tuple, Optional, List
from os import get_terminal_size

logger = get_logger(__name__)

DB = './config/test.db'


class CourseDb:
    def __init__(self, db_path: str) -> None:
        self.db_path = Path(db_path).absolute()
        if not self.db_exists():
            self.create_db()

    def db_exists(self) -> bool:
        return self.db_path.absolute().exists()

    def create_db(self):
        if not self.db_path.parent.exists():
            self.db_path.parent.mkdir()
            logger.info(
                f'created config directory {self.db_path.parent}'
            )

        create_query = '''
            CREATE TABLE course (
                course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT (datetime('now','localtime')),
                name VARCHAR NOT NULL,
                current_task VARCHAR,
                next_task VARCHAR
            );
        '''
        self.execute_query(create_query)
        self.execute_query('''
            CREATE TRIGGER course_trig AFTER UPDATE ON course
            BEGIN
                update course set timestamp = datetime('now')
                WHERE course_id = NEW.course_id;
            END;
        ''')
        logger.info(f'db {self.db_path} created successfully')

    def execute_query(
        self,
        query: str,
        values: Optional[Tuple[Optional[str], ...]] = None
    ) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            if values:
                cur.execute(query, values)
            else:
                cur.execute(query)
            conn.commit()
            cur.close()

    def add_course(
        self,
        name: str,
        current_task: str = None,
        next_task: str = None
    ) -> None:
        self.execute_query('''
            INSERT INTO course (name, current_task, next_task)
            VALUES (?, ?, ?)
        ''', (name, current_task, next_task))

    def remove_course(self, course_id: str) -> None:
        self.execute_query('''
            DELETE FROM course WHERE course_id=?
        ''', (course_id,))

    def update_course(
        self,
        course_id: str,
        name: str = None,
        current_task: str = None,
        next_task: str = None
    ) -> None:
        update_fields = []
        update_values = []
        if name:
            update_fields.append('name=?')
            update_values.append(name)
        if current_task:
            update_fields.append('current_task=?')
            update_values.append(current_task)
        if next_task:
            update_fields.append('next_task=?')
            update_values.append(next_task)

        update_values.append(course_id)
        query = f'''
            UPDATE course
            SET {', '.join(update_fields)}
            WHERE course_id=?
        '''
        self.execute_query(query, tuple(update_values))

    def fetch_all(self) -> List:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM course')
            results = cur.fetchall()
        return results

    def print_table(self):
        terminal_width = get_terminal_size().columns
        print('[Courses]'.center(terminal_width))
        print('-' * terminal_width)
        field_width = terminal_width // 5
        headings = [
            'Course ID', 'Last Modified', 'Name',
            'Current Task', 'Next Task'
        ]
        for heading in headings:
            print(f'[{heading}]'.ljust(field_width), end='')
        print('\n')

        rows = self.fetch_all()
        for row in rows:
            for item in row:
                print(str(item).ljust(field_width), end='')
            print()

        if len(rows) == 0:
            logger.info('Empty Database')
