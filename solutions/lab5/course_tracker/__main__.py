from course_tracker.cli import CourseTrackerCLI
from course_tracker.services import Course


def main() -> None:
    course = Course()
    cli = CourseTrackerCLI(course)
    cli.run()


if __name__ == "__main__":
    main()