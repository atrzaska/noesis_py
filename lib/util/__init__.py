import os
import struct

def logNotImplementedMethod(name, args):
    if os.environ.get('DEBUG') == 'true':
        print("Not implemented method called: " + name, args)

def last(arr):
    return arr[-1] if len(arr) > 0 else None

def dump(path, data):
    handle = open(path, 'wb')
    handle.write(data)
    handle.close()

def floatToHalfFloat(float32):
    F16_EXPONENT_BITS = 0x1F
    F16_EXPONENT_SHIFT = 10
    F16_EXPONENT_BIAS = 15
    F16_MANTISSA_BITS = 0x3ff
    F16_MANTISSA_SHIFT =  (23 - F16_EXPONENT_SHIFT)
    F16_MAX_EXPONENT =  (F16_EXPONENT_BITS << F16_EXPONENT_SHIFT)

    a = struct.pack('>f',float32)
    b = binascii.hexlify(a)

    f32 = int(b,16)
    f16 = 0
    sign = (f32 >> 16) & 0x8000
    exponent = ((f32 >> 23) & 0xff) - 127
    mantissa = f32 & 0x007fffff

    if exponent == 128:
        f16 = sign | F16_MAX_EXPONENT
        if mantissa:
            f16 |= (mantissa & F16_MANTISSA_BITS)
    elif exponent > 15:
        f16 = sign | F16_MAX_EXPONENT
    elif exponent > -15:
        exponent += F16_EXPONENT_BIAS
        mantissa >>= F16_MANTISSA_SHIFT
        f16 = sign | exponent << F16_EXPONENT_SHIFT | mantissa
    else:
        f16 = sign
    return f16

def halfFloatToFloat(float16Data):
    s = int((float16Data >> 15) & 0x00000001)    # sign
    e = int((float16Data >> 10) & 0x0000001f)    # exponent
    f = int(float16Data & 0x000003ff)            # fraction

    if e == 0:
        if f == 0:
            return int(s << 31)
        else:
            while not (f & 0x00000400):
                f = f << 1
                e -= 1
            e += 1
            f &= ~0x00000400
            #print(s,e,f)
    elif e == 31:
        if f == 0:
            return int((s << 31) | 0x7f800000)
        else:
            return int((s << 31) | 0x7f800000 | (f << 13))

    e = e + (127 -15)
    f = f << 13
    temp = int((s << 31) | (e << 23) | f)
    packed = struct.pack('I', temp)
    return struct.unpack('f', packed)[0]

def halfFloatsToFloats(values):
    return map(lambda x: halfFloatToFloat(x), values)
