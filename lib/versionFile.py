import os, shutil
def versionFile(file_spec, vtype='copy'):
    if os.path.isfile(file_spec):
        # or, do other error checking:
        if vtype not in ['copy', 'rename']:
            vtype = 'copy'

        # Determine root filename so the extension doesn't get longer
        n, e = os.path.splitext(file_spec)

        # Is e an integer?
        try:
            num = int(e)
            root = n
        except ValueError:
            root = file_spec

        # Find next available file version
        for i in xrange(1000):
            new_file = '%s.%03d' % (root, i)
            if not os.path.isfile(new_file):
                if vtype == 'copy':
                    shutil.copy(file_spec, new_file)
                else:
                    os.rename(file_spec, new_file)
                return 1

    return 0

if __name__ == '__main__':
# test code (you will need a file named test.txt)
    print versionFile('test.txt')
    print versionFile('test.txt')
    print versionFile('test.txt')