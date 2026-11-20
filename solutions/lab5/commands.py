from sys import exit

def exiting():
    exit(0)

def help_text():
    text = ("""
    Здесь должен быть текст, но он пока не придуман
    """)

def commands_analyzer(line):
    raw_line = line.strip().split()
    main_command = raw_line[0]
    match main_command:
        case "help":
            help_text()
        case "exit":
            exiting()
        case "student":
            pass
        case "lab":
            pass
        case "submit":
            pass
        case "submission":
            pass
        # После report может быть команда top 5, как её обрабатывать?
        # Выводить топ 5 лучших студентов?
        case "report":
            pass
        case "import":
            pass
        case "export":
            pass
        case "snapshot":
            pass
        case "undo":
            pass
        case "memory":
            pass
        case _:
            print("Неизвестная команда")
