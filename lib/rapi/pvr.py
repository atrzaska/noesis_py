import sys
import numpy as np
import io
from bitstring import ConstBitStream

def scaleTo255(color, size):
    number = float(color) / 2**size
    return int(number * 255)

def compact(x):
    x &= 0x55555555                  # x = -f-e -d-c -b-a -9-8 -7-6 -5-4 -3-2 -1-0
    x = (x ^ (x >> 1)) & 0x33333333  # x = --fe --dc --ba --98 --76 --54 --32 --10
    x = (x ^ (x >> 2)) & 0x0f0f0f0f  # x = ---- fedc ---- ba98 ---- 7654 ---- 3210
    x = (x ^ (x >> 4)) & 0x00ff00ff  # x = ---- ---- fedc ba98 ---- ---- 7654 3210
    x = (x ^ (x >> 8)) & 0x0000ffff
    return x

def decodeMorton(i):
    x = compact(i)
    y = compact(i >> 1)
    return x, y

IMG_SCALE = 8
MOD_SCALE = 2

def decode(pvrData, width, height, bpp):
    mip = 1
    image_width = width // 4 // 2**(mip)
    image_height = height // 4 // 2**(mip)

    bit_stream = ConstBitStream(bytes=pvrData)

    # RGBA pixel buffers indexed [y, x]
    img_a = np.zeros((height // IMG_SCALE, width // IMG_SCALE, 4), dtype=np.uint8)
    img_b = np.zeros((height // IMG_SCALE, width // IMG_SCALE, 4), dtype=np.uint8)
    img_mod = np.zeros((height // MOD_SCALE, width // MOD_SCALE, 4), dtype=np.uint8)

    for i in range(image_width * image_height):
        pixel, row = decodeMorton(i)
        modulation_data = bit_stream.read('bits:32')

        byte0 = bit_stream.read('bits:8')
        byte1 = bit_stream.read('bits:8')
        byte2 = bit_stream.read('bits:8')
        byte3 = bit_stream.read('bits:8')
        color_mode = byte3.read('bool')

        r = g = b = a = 255
        if color_mode:
            r = byte3.read('uint:5')
            g = (byte3.read('bits:2') + byte2.read('bits:3')).read('uint:5')
            b = byte2.read('uint:5')
            r = scaleTo255(r, 5)
            g = scaleTo255(g, 5)
            b = scaleTo255(b, 5)
        else:
            a = byte3.read('uint:3')
            r = byte3.read('uint:4')
            g = byte2.read('uint:4')
            b = byte2.read('uint:4')
            a = scaleTo255(a, 3)
            r = scaleTo255(r, 4)
            g = scaleTo255(g, 4)
            b = scaleTo255(b, 4)
        img_b[pixel, row] = (r, g, b, a)

        color_mode = byte1.read('bool')


        r = g = b = a = 255
        if color_mode:
            r = byte1.read('uint:5')
            g = (byte1.read('bits:2') + byte0.read('bits:3')).read('uint:5')
            b = byte0.read('uint:4')
            r = scaleTo255(r, 5)
            g = scaleTo255(g, 5)
            b = scaleTo255(b, 4)
        else:
            a = byte1.read('uint:3')
            r = byte1.read('uint:4')
            g = byte0.read('uint:4')
            b = byte0.read('uint:3')
            a = scaleTo255(a, 3)
            r = scaleTo255(r, 4)
            g = scaleTo255(g, 4)
            b = scaleTo255(b, 3)

        img_a[pixel, row] = (r, g, b, a)

        mode = byte0.read('bool')

        for r in range(4):
            for c in range(4):
                first = modulation_data.read('uint:1')
                last = modulation_data.read('uint:1')
                value = 0
                if first == 0 and last == 0:
                    value = 0
                elif first == 0 and last == 1:
                    value = 3
                elif first == 1 and last == 0:
                    value = 5
                elif first == 1 and last == 1:
                    value = 8
                texel_row = 3 - r + row*4
                texel_col = 3 - c + pixel*4
                img_mod[texel_col, texel_row] = (0, 0, 0, int(float(value)/8*255))

    return img_a.tobytes()
