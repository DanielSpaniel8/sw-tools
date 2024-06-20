import os

programs = b''

with open('./cat_programs.scl', 'rb') as file:
    programs = file.read()


content = b''

for match in os.scandir('.'):
    if match.name.split('.')[1] == 'lua':
        with open(match, 'rb') as file:
            content += (b'-- #@# '+bytes(match.name, 'ascii')+b'\n      \n')
            content += file.read()
            
if len(content) > 1_000_000:
    print('your code is too long!')
    quit()

chunk_start = 8888
before = programs[:chunk_start]
after = programs[chunk_start+len(content):]

full_data = before + content + after


with open('./cat_out.scl', 'wb') as file:
   file.write(full_data)
