def recover_data(drive, type_of_file, file_format, signature, EOF_signature):
    fileD = open(drive, 'rb')
    size = 512
    byte = fileD.read(size)
    offs = 0
    drec = False
    rcvd = 0

    count = 0

    while byte:
        found = byte.find(signature)

        if found >= 0:
            drec = True
            print('==== Found ' + type_of_file + ' at location: ' + str(hex(found + (size * offs))) + ' ====')
            fileN = open(f'{drive}\\recovered_files\\' + str(rcvd) + file_format, "wb")
            fileN.write(byte[found:])
            while drec:
                byte = fileD.read(size)
                if EOF_signature:
                    bfind = byte.find(EOF_signature)
                    if bfind >= 0:
                        fileN.write(byte[:bfind + 2])
                        fileD.seek((offs + 1) * size)
                        print('==== Wrote ' + type_of_file + ' at location: ' + str(rcvd) + file_format + ' ====')
                        count += 1
                        drec = False
                        rcvd += 1
                        fileN.close()
                    else:
                        fileN.write(byte)
                else:
                    fileN.write(byte)
                    print('==== Wrote ' + type_of_file + ' at location: ' + str(rcvd) + file_format + ' ====')
                    count += 1
                    drec = False
                    rcvd += 1
                    fileN.close()
        else:
            byte = fileD.read(size)

        offs += 1

    fileD.close()

if __name__ == '__main__':
    signatures = [
        {
            'index': 0,
            'type_of_file': 'PDF',
            'file_format': '.pdf',
            'file_signature': b'\x25\x50\x44\x46',
            'EOF': b'\x25\x25\x45\x4f\x46',
        },
        {
            'index': 1,
            'type_of_file': 'JPG',
            'file_format': '.jpg',
            'file_signature': b'\xff\xd8\xff\xe0\x00\x10\x4a\x46',
            'EOF': b'\xff\xd9',
        },
        {
            'index': 2,
            'type_of_file': 'PNG',
            'file_format': '.png',
            'file_signature': b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a',
            'EOF': None,
        },
        # {
        #     'type_of_file': 'TXT',
        #     'file_format': '.txt',
        #     'file_signature': b'\x00\x00\xFE\xFF',
        #     'EOF': None,
        # },
        # {
        #     'type_of_file': 'ZIP',
        #     'file_format': '.zip',
        #     'file_signature': b'\x50\x4b\x03\x04',
        #     'EOF': b'\x50\x4b\x05\x06',
        # },
    ]
    
    drive = "\\\\.\\F:"
    signature = signatures[0]
    print('Started reading '+ signature.get('type_of_file') + ' files...')
    recover_data(
        drive,
        signature.get('type_of_file'),
        signature.get('file_format'),
        signature.get('file_signature'),
        signature.get('EOF')
    )
