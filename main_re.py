import re
import time


start_time = time.perf_counter()
for _ in range(100):
    with open('timetable.json', 'r', encoding='utf-8') as json_file:
        with open('timetable.yaml', 'w', encoding='utf-8') as yaml_file:
            for current_string in json_file.read().split('\n'):
                if len(re.findall(r'":', current_string)) >= 1:
                    current_string = re.sub(r'[{}"",]', '', current_string)
                    yaml_file.write(current_string[2:] + '\n')
print(time.perf_counter() - start_time)
