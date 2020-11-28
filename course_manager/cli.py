import argparse
import sys
from course_manager.db import CourseDb
from course_manager.db import DB
from course_manager.logger import get_logger
from typing import Optional, Sequence

logger = get_logger(__name__)


def main(argv: Optional[Sequence[str]] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(description='Course Manager')
    subparsers = parser.add_subparsers(help='commands', dest='command')
    add_parser = subparsers.add_parser('add', help='Add a course')
    remove_parser = subparsers.add_parser('remove', help='Remove a course')
    update_parser = subparsers.add_parser('update', help='Update a course')
    list_parser = subparsers.add_parser('list', help='List courses')
    help_parser = subparsers.add_parser('help',
                                        help='Display help for a command')

    add_parser.add_argument('name', help='Name of the course')
    add_parser.add_argument('-c', '--current', help='Set current task')
    add_parser.add_argument('-n', '--next',  help='Set next task')

    remove_parser.add_argument('course_id', nargs='?',
                               help='Remove a course by ID')
    remove_parser.add_argument('-a', '--all', action='store_true',
                               help='Remove all courses')

    update_parser.add_argument('course_id', help='ID of course to update')
    update_parser.add_argument('--name',
                               help='Name of the updated course')
    update_parser.add_argument('-c', '--current',
                               help='New current task')
    update_parser.add_argument('-n', '--next',
                               help='New next task')

    help_parser.add_argument('cmd', help='command name to get help for')

    args = parser.parse_args(argv)
    course_db = CourseDb(DB)
    if args.command == 'add':
        course_db.add_course(name=args.name, current_task=args.current,
                             next_task=args.next)
    elif args.command == 'remove':
        if args.all:
            course_db.remove_course('ALL')
        elif args.course_id:
            course_db.remove_course(args.course_id)
        else:
            remove_parser.print_help()
    elif args.command == 'update':
        course_db.update_course(course_id=args.course_id, name=args.name,
                                current_task=args.current,
                                next_task=args.next)
    elif args.command == 'list':
        course_db.print_table()
    elif args.command == 'help':
        if args.cmd in subparsers.choices:
            subparsers.choices[args.cmd].print_help()
        else:
            logger.error(f'command {args.cmd!r} not found')
            return 1
    else:
        parser.print_help()

    return 0


if __name__ == '__main__':
    exit(main())
