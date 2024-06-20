from struct import pack, unpack
from os import system as command
from os import get_terminal_size as size

cbb = '\033[1;44;97m'
cR  = '\033[0m'

horizontal = '─'
vertical = '│'
tl_corner = '┌'
tr_corner = '┐'
bl_corner = '└'
br_corner = '┘'


def pack_float(num):
    h = ''
    for i in pack("<f", num):
        h += hex(i)[2:].zfill(2) + ' '
    return h

def unpack_float(num):
    
    n = b''
    for i in range(4):
        b = int(num[:2], base=16)
        b = bytes([b])
        n += b
        num = num[2:]
    return str(unpack("<f", n)[0])
            
def pack_varint(num):

    blist = []

    while num != 0:
        b = num % 128
        if num < 128:
            blist.append(b)

            output = ''
            for i in bytes(blist):
                output += hex(i)[2:].zfill(2) + ' '
            return output
        
        num = num // 128
        blist.append(b+128)

def unpack_varint(num):

    value  = 0   # value of the pointer, to be returned
    offset = 0   # how many bytes were in the varInt, to be advanced later

    b = int(num[:2], base=16)
    num = num[2:]
    value = b

    while b > 127:   # continue until lack of continuation bit

        offset +=1
        value -= 128 ** offset   # subtract the value of the last byte's continuation bit

        b = int(num[:2], base=16)
        value += b * (128 ** offset)

    return str(value)

def check_input(input):

    global error
    match mode:
        case 'df':
            try:
                t = float(input)
            except:
                error = 'not dec'
                return True
        case 'dh'|'dv':
            try:
                t = int(input)
            except:
                error = 'not int'
                return True
    match mode[0]:
        case 'h'|'v':
            try:
                t = int(input, base=16)
            except:
                error = 'not hex'
                return True
        case 'f':
            try:
                t = int(input, base=16)
            except:
                error = 'not hex'
                return True
            if not len(input) == 8:
                error = 'short  '
                return True

    return False

def check_mode():

    global mode
    global error

    modes = ['d','h','f','v']

    if not mode[0] in modes:
        mode = 'd'+mode[1]
        error = 'ch mode'
    if not mode[1] in modes:
        mode = mode[0]+'f'
        error = 'ch mode'

def match_mode(input):

    match mode:

        # dec
        case 'dd':
            history.append(  input  )
        case 'dh':
            history.append(  str( int(input, base=16) )  )
        case 'df':
            n = float(input)
            history.append(  pack_float(n)  )
        case 'dv':
            n = int(input)
            history.append(  pack_varint(n)  )

        # hex
        case 'hd':
            history.append(  str(int(input, base=16)))
        case 'hh':
            history.append(  input  )
        case 'hf':
            n = int(input, base=16)
            history.append(  pack_float(n)  )
        case 'hv':
            n = int(input, base=16)
            history.append(  pack_varint(n)  )

        # float
        case 'fd':
            history.append(  unpack_float(input)  )
        case 'fh':
            history.append(  unpack_float(input)  )
        case 'ff':
            history.append(  input  )
        case 'fv':
            history.append(   pack_varint( int(float(unpack_float(input))) )  )
            
        # varint
        case 'vd':
            history.append(  unpack_varint(input)  )            
        case 'vh':
            history.append(  unpack_varint(input)  )            
        case 'vf':
            history.append(  pack_float(int(unpack_varint(input)))  )
        case 'vv':
            history.append(  input  )

    display()

def display():

    global error

    width = size().columns
    height = size().lines

    command('clear')


    print(tl_corner+horizontal*(width-2)+tr_corner)

    # full history
    if len(history) > (height-4):
        
        for i in history[height-4:]:
            print('|',i.ljust(width),'|')
        
    # not full history
    else:
        
        for i in range((height-3)-(len(history)*2)): # empty lines
            print(vertical+' '*(width-2)+vertical)
        for i in history:                            # history lines  
            print(vertical+' '*(width-2)+vertical)
            print(vertical+' '+i.ljust(width-3)+vertical)

    if error == '':

        starting_decor = bl_corner+cbb+horizontal
        mode_inf = mode.ljust(width-3, horizontal)
        ending_decor = cR+br_corner

        print(starting_decor+mode_inf+ending_decor)

    else:
    
        starting_decor = bl_corner+cbb+horizontal
        mode_inf = mode.ljust(width-12, horizontal)
        error_inf = error+horizontal*2
        ending_decor = cR+br_corner

        error = ''

        print(starting_decor+mode_inf+error_inf+ending_decor)

def help():
    command('clear')

    help_lines = [
        'enter values to have them converted',
        'enter a single letter to change input mode',
        'enter two letters to change input and output modes',
        'modes are:',
        'd=decimal/h=hex/f=float/v=varint',
        'e.g. "hf" will convert hex to a packed float',
        '',
        'error codes (shown at the bottom-right):',
        '"ch mode":',
        '  you entered the wrong letter and it went to the default',
        '"not dec", "not hex", "not int":',
        '  the value you entered can\'t be converted',
        '"short":',
        '  the value you entered is too short (make it 8 chars)',
        '',
        'enter "colours" to toggle ansi colours',
        'this might help if the output looks broken',
        '',
        'enter "e" to exit the script',
        ]
    
    print(tl_corner+horizontal*(width-2)+tr_corner)
        
    for i in range(height-(len(help_lines)+3)): # empty lines
        print(vertical+' '*(width-2)+vertical)
    for i in help_lines: # help lines
        print(vertical+' '+i.ljust(width-3)+vertical)

    starting_decor = bl_corner+cbb+horizontal
    mode_inf = mode.ljust(width-14, horizontal)
    help_msg = 'help page'+horizontal*2
    ending_decor = cR+br_corner

    print(starting_decor+mode_inf+help_msg+ending_decor)

    exit = input('press enter to close help page] ')



uin = ''
mode = 'df'
error = ''
colours = True

history = ['']

while uin != 'e':

    width = size().columns
    height = size().lines

    display()

    uin = input("] ")
    if uin == 'e':
        command('clear')
        quit()

    if uin=='help':
        help()
        continue
    
    if uin=='colours' or uin=='colors':
        if colours:
            colours = False
            cbb=''
            cR=''
            error = 'clr off'
        else:
            colours = True
            cbb = '\033[1;44;97m'
            cR  = '\033[0m'
            error = 'clr  on'


    if len(uin)==1 and uin.isalpha() and uin[0] != 'x':
        mode = uin + mode[1]
        check_mode()
        continue

    if len(uin)==2 and uin.isalpha() and uin[0] != 'x':
        mode = uin
        check_mode()
        continue

    if uin[0] == 'x':
        uin = uin[1:]

    if check_input(uin):
        continue


    match_mode(uin)

