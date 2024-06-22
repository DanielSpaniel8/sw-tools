# --- swordigo quest generator v2

with open('./itemvar_gamedata.gdata', 'rb') as file:
    gamedata = file.read()

machine_name = input('machine name: ')
title = input('title: ')
target_level = input('target level: ')

quest = b''

quest_size = len(machine_name)+len(title)+len(target_level)
quest_size += 6

# add quest tag and overall pointer
quest += b'\x1a'+ bytes([quest_size])

# add quest data with tags and pointers
quest += b'\x0a'+ bytes([len(machine_name)])+ bytes(machine_name, 'ascii')

quest += b'\x12'+ bytes([len(title)])+ bytes(title, 'ascii')

quest += b'\x22'+ bytes([len(target_level)])+ bytes(target_level, 'ascii')

out_data = quest + gamedata

with open('./quest_out.gdata', 'wb') as file:
    file.write(out_data)

print('done')
