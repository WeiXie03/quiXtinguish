import os
import uncompyle6
your_directory = ''
for dirpath, b, filenames in os.walk(your_directory):
    for filename in filenames:
        print(filename)
        if not filename.endswith('.pyc'):
            continue
            print('none in ', filenames)

        filepath = dirpath + '/' + filename
        original_filename = filename.split('.')[0]
        original_filepath = dirpath + '/' + original_filename + '.py'
        with open(original_filepath, 'w') as f:
            uncompyle6.decompile_file(filepath, f)
        print('yes')
