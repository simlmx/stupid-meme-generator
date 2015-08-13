import subprocess, sys, os

# http://stackoverflow.com/a/20380514/1067132
import struct
import imghdr

def get_image_size(fname):
    '''Determine the image type of fhandle and return its size.
    from draco'''
    fhandle = open(fname, 'rb')
    head = fhandle.read(24)
    if len(head) != 24:
        raise TypeError
    if imghdr.what(fname) == 'png':
        check = struct.unpack('>i', head[4:8])[0]
        if check != 0x0d0a1a0a:
            raise TypeError
        width, height = struct.unpack('>ii', head[16:24])
    elif imghdr.what(fname) == 'gif':
        width, height = struct.unpack('<HH', head[6:10])
    elif imghdr.what(fname) == 'jpeg':
        fhandle.seek(0)  # Read 0xff next
        size = 2
        ftype = 0
        while not 0xc0 <= ftype <= 0xcf:
            fhandle.seek(size, 1)
            byte = fhandle.read(1)
            while ord(byte) == 0xff:
                byte = fhandle.read(1)
            ftype = ord(byte)
            size = struct.unpack('>H', fhandle.read(2))[0] - 2
        # We are at a SOFn block
        fhandle.seek(1, 1)  # Skip `precision' byte.
        height, width = struct.unpack('>HH', fhandle.read(4))
    else:
        raise TypeError
    return width, height


def rescale_image(filename, output_filename, max_dim):
    width, height = get_image_size(filename);
    w_max = width >= height
    new_dim = [max_dim,max_dim]
    if w_max:
        new_dim[0] = -1
    else:
        new_dim[1] = -1
    scale = '{}:{}'.format(*new_dim)
    subprocess.call(['ffmpeg','-i',filename,'-vf','scale='+scale,
                    output_filename])


if __name__ == '__main__':
    # arg 1 : input file
    # arg2 : output dir

    image = sys.argv[1]
    output_dir = sys.argv[2]

    max_ = 256
    thumb_max = 128
    new_ext='.jpg'

    filename = os.path.basename(image)
    name,ext = os.path.splitext(filename)
    filename = name + new_ext
    thumb_filename = name + '_t' + new_ext
    rescale_image(
        image,
        os.path.join(output_dir,filename),
        max_)
    rescale_image(
        image,
        os.path.join(output_dir, thumb_filename),
        thumb_max)
