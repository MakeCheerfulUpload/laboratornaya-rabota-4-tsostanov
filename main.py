import time

all_time = 0


def get_information(pattern_information, information):
    pattern_keys = [i for i in pattern_information.keys()]
    while '"' in information:
        delta = information[:information.index('"')]
        information = information[(information.index('"') + 1):]
        if delta in pattern_keys:
            information = information[(information.index('"') + 1):]
            pattern_information[delta] = information[:information.index('"')]
    return pattern_information


def about_timetable(information):
    pattern_information = {'lang': None,
                           'group': None,
                           'day': None,
                           'lessons': None
                           }
    return get_information(pattern_information, information)


def about_lesson(information):
    pattern_information = {'time': None,
                           'room': None,
                           'place': None,
                           'lesson': None,
                           'type': None,
                           'teacher': None
                           }
    return get_information(pattern_information, information)


def start(json_file, yaml_file):
    global all_time
    start_time = time.perf_counter()
    flag_timetable = False
    nesting_level = -1
    input_file = open(json_file, 'r', encoding='utf-8')
    output_file = open(yaml_file, 'w', encoding='utf-8')
    for lines in input_file.read().replace('{', '!{').replace('}', '}!').split('!'):
        nesting_level += lines.count('{')
        if lines.count(':') == 1:
            current_line = lines[(lines.index('"') + 1):-2]
            output_file.write(' ' * nesting_level * 2 + current_line + ':\n')
        elif lines.count(':') > 1:
            if flag_timetable:
                for key, value in about_lesson(lines).items():
                    output_file.write(' ' * nesting_level * 2 + "{0}: {1}".format(key, value) + '\n')
            else:
                for key, value in about_timetable(lines + '""').items():
                    output_file.write(' ' * nesting_level * 2 + "{0}: {1}".format(key, value) + '\n')
                flag_timetable = True
        nesting_level -= lines.count('}')
    input_file.close()
    output_file.close()
    all_time += time.perf_counter() - start_time


for _ in range(100):
    start('re_timetable.json', 'timetable.yaml')
print(all_time)
