gamedata = b''
with open('./itemvar_gamedata.gdata', 'rb') as file:
    gamedata = file.read()

name = input('variable name: ')

new_item = b'\x0a' + bytes([len(name)+10])
new_item += b'\x08\x05'

new_item += b'\x12'+ bytes([len(name)]) + bytes(name, 'ascii')
new_item += b'\x1a\x01-'
new_item += b'\x2a\x01-'

out_data = new_item+gamedata

with open ('./out.gdata', 'wb') as file:
    file.write(out_data)

print('done')
