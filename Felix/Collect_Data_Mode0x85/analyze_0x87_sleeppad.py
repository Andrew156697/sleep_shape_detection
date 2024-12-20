import time
import  csv

'''Response: 
The device sends frame type [0x87], content 6byte: [mode 1byte] + [error 1byte] + [4byte time]
- Mode [1byte]: =0x00 stands for standby mode;=0x20 stands for server monitoring mode;
                =0x30 stands for data debugging mode;=0x40 stands for BLE, =0xF0 means waiting for firmware update;
debugging mode;
- Error [1byte]: =0x00 means no error;
                =any other value means the device is faulty and needs to be returned to the factory

'''

demo_0x87 = "7D 87 15 00 55 4E 43 4F 4E 46 49 47 45 44 00 00 3B C2 3A 63 0D"
demo_0x87 = demo_0x87.replace(" ", "")
print(demo_0x87)

define_mode = ['Stands for standby mode', 'Stands for server monitoring mode', 'Stands for data debugging mode',
               'Stands for BLE debugging mode', 'Waiting for firmware update']
define_error = ['No error', 'The device is faulty and must to be returned to the factory']

print('Length: ', len(demo_0x87))

time_current = time.strftime("%H:%M:%S")
day_current = time.strftime("%d/%m/%Y")
print('Time Now LAPTOP: ', time_current)
print('Day Now LAPTOP: ', day_current)

header = demo_0x87[0:2]
type_frame = demo_0x87[2:4]
length_frame = demo_0x87[4:8]
id_total = demo_0x87[8:28]
content = demo_0x87[28: -2]
end = demo_0x87[-2:]

print('Header: ' , header)
print('Type_frame: ', type_frame)
print('Length_frame: ', length_frame)
print('ID total: ', id_total)
print('Content: ', content)
print('End: ', end)


# analyze content
mode = content[0:2]
error = content[2:4]
time_hex = content[4:]

print("Mode hex: ", mode)
print("Error hex: ", error)
print("Time hex : ", time_hex)





def convert_mode_real_value(data_hex_mode):
    if data_hex_mode == '00':
        return define_mode[0]
    elif data_hex_mode == '20':
        return define_mode[1]
    elif data_hex_mode == '30':
        return define_mode[2]
    elif data_hex_mode == '40':
        return define_mode[3]
    elif data_hex_mode == 'F0':
        return data_hex_mode[4]

def convert_error_real_value(data_hex_error):
    if data_hex_error == '00':
        return define_error[0]
    else:
        return define_error[1]
    
print('Mode real: ', convert_mode_real_value(mode))
print('Error real: ', convert_error_real_value(error))