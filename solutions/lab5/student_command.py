def student_command_analyzer(line):
    raw_line = line.strip().split()
    main_command = raw_line[0]
    sub_command = raw_line[1]
    match sub_command:
        case "add":
            pass
        case "list":
            pass
        case "show":
            pass
        case "deactivate":
            pass
        case "activate":
            pass
        case "search":
            pass
        case _:
            print("Некорректные аргументы")