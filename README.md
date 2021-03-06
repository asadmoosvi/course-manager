# course manager

Keep track of the courses you're taking with a current task and next task
for each.

# installation
`pip install .` for the latest dev version or `pip install course-manager` for
the stable release.

# usage

## help menu
```
usage: course_manager [-h] {add,remove,update,list} ...

Course Manager

positional arguments:
  {add,remove,update,list}
                        commands
    add                 Add a course
    remove              Remove a course
    update              Update a course
    list                List courses

optional arguments:
  -h, --help            show this help message and exit
```

## asciinema example
[![asciicast](https://asciinema.org/a/bUzn4Mrhz2Kk1eVcaGtkZSIp3.svg)](https://asciinema.org/a/bUzn4Mrhz2Kk1eVcaGtkZSIp3)

## list all courses
`course_manager list`

## add courses
`course_manager add 'learn python'`

`course_manager add 'learn python' -c 'chapter 1' -n 'chapter 5'`

## remove a course by id
`course_manager remove 1`

## update a course
`course_manager update 1 --next 'watch lecture 2'`
