# Image decoding helpers backing rapi.imageDecodeDXT / imageDecodeRaw / imageFlipRGBA32.
# Pure numpy; output is RGBA32 bytes (row 0 first, as stored).
import re

import numpy as np

import noesis


def _blocks(data, width, height, blockBytes):
    bw, bh = max(1, (width + 3) // 4), max(1, (height + 3) // 4)
    raw = np.frombuffer(bytes(data[:bw * bh * blockBytes]), dtype=np.uint8)
    return raw.reshape(bh, bw, blockBytes), bw, bh


def _toImage(texels, bw, bh, width, height):
    """texels: (bh, bw, 16, 4) -> (height, width, 4) uint8 RGBA bytes."""
    img = texels.reshape(bh, bw, 4, 4, 4).transpose(0, 2, 1, 3, 4).reshape(bh * 4, bw * 4, 4)
    return np.ascontiguousarray(img[:height, :width]).tobytes()


def _color(block, punchThrough):
    """BC1 colour block (bh, bw, 8 bytes) -> (bh, bw, 16, 4) RGBA."""
    c = block[..., 0:4].copy().view("<u2")  # (bh, bw, 2): c0, c1
    c0, c1 = c[..., 0].astype(np.int32), c[..., 1].astype(np.int32)

    def expand(v):
        r = ((v >> 11) & 31) * 255 // 31
        g = ((v >> 5) & 63) * 255 // 63
        b = (v & 31) * 255 // 31
        return np.stack([r, g, b], axis=-1)

    e0, e1 = expand(c0), expand(c1)
    four = (c0 > c1) | (not punchThrough)
    four = np.broadcast_to(four, c0.shape)[..., None]
    # DXT1 rounds the thirds, DXT3/5 colour blocks truncate (matches Pillow's decoders)
    r = 1 if punchThrough else 0
    p2 = np.where(four, (2 * e0 + e1 + r) // 3, (e0 + e1) // 2)
    p3 = np.where(four, (e0 + 2 * e1 + r) // 3, 0)
    palette = np.stack([e0, e1, p2, p3], axis=-2)  # (bh, bw, 4, 3)
    alpha = np.full(palette.shape[:-1] + (1,), 255)
    if punchThrough:
        alpha[..., 3, 0] = np.where(four[..., 0], 255, 0)
    palette = np.concatenate([palette, alpha], axis=-1)
    bits = block[..., 4:8].copy().view("<u4")[..., 0].astype(np.int64)
    idx = (bits[..., None] >> (2 * np.arange(16))) & 3  # (bh, bw, 16)
    return np.take_along_axis(palette, idx[..., None].repeat(4, axis=-1), axis=-2).astype(np.uint8)


def _bc4(block):
    """BC4 single channel block (bh, bw, 8 bytes) -> (bh, bw, 16) uint8."""
    a0, a1 = block[..., 0].astype(np.int32), block[..., 1].astype(np.int32)
    eight = (a0 > a1)[..., None]
    i = np.arange(1, 7)
    interp8 = ((7 - i) * a0[..., None] + i * a1[..., None]) // 7       # 6 values
    j = np.arange(1, 5)
    interp6 = ((5 - j) * a0[..., None] + j * a1[..., None]) // 5       # 4 values
    pad6 = np.concatenate([interp6, np.zeros_like(a0)[..., None], np.full_like(a0, 255)[..., None]], axis=-1)
    palette = np.concatenate([a0[..., None], a1[..., None], np.where(eight, interp8, pad6)], axis=-1)
    raw = block[..., 2:8].astype(np.int64)
    bits = sum(raw[..., k] << (8 * k) for k in range(6))
    idx = (bits[..., None] >> (3 * np.arange(16))) & 7
    return np.take_along_axis(palette, idx, axis=-1).astype(np.uint8)


def decodeDXT(data, width, height, fourcc):
    if fourcc == noesis.FOURCC_DXT1:
        blocks, bw, bh = _blocks(data, width, height, 8)
        return _toImage(_color(blocks, True), bw, bh, width, height)
    if fourcc == noesis.FOURCC_DXT3:
        blocks, bw, bh = _blocks(data, width, height, 16)
        texels = _color(blocks[..., 8:16], False)
        nib = blocks[..., 0:8].astype(np.int64)
        bits = sum(nib[..., k] << (8 * k) for k in range(8))
        texels[..., 3] = (((bits[..., None] >> (4 * np.arange(16))) & 15) * 17).astype(np.uint8)
        return _toImage(texels, bw, bh, width, height)
    if fourcc == noesis.FOURCC_DXT5:
        blocks, bw, bh = _blocks(data, width, height, 16)
        texels = _color(blocks[..., 8:16], False)
        texels[..., 3] = _bc4(blocks[..., 0:8])
        return _toImage(texels, bw, bh, width, height)
    if fourcc == noesis.FOURCC_ATI1:
        blocks, bw, bh = _blocks(data, width, height, 8)
        v = _bc4(blocks)
        texels = np.stack([v, v, v, np.full_like(v, 255)], axis=-1)
        return _toImage(texels, bw, bh, width, height)
    if fourcc == noesis.FOURCC_ATI2:
        blocks, bw, bh = _blocks(data, width, height, 16)
        r, g = _bc4(blocks[..., 0:8]), _bc4(blocks[..., 8:16])
        texels = np.stack([r, g, np.zeros_like(r), np.full_like(r, 255)], axis=-1)
        return _toImage(texels, bw, bh, width, height)
    return None


def decodeRaw(data, width, height, fmt):
    """Noesis channel format strings, e.g. "r8g8b8", "b8g8r8a8", "r5g6b5" (first channel = lowest bits)."""
    channels = re.findall(r"([rgbap])(\d+)", fmt.lower())
    bits = sum(int(b) for _, b in channels)
    if not channels or bits % 8 or bits > 64:
        return None
    pixelBytes = bits // 8
    n = width * height
    raw = np.frombuffer(bytes(data[:n * pixelBytes]), dtype=np.uint8).reshape(n, pixelBytes).astype(np.uint64)
    value = sum(raw[:, k] << np.uint64(8 * k) for k in range(pixelBytes))
    out = np.zeros((n, 4), dtype=np.uint8)
    out[:, 3] = 255
    shift = 0
    for ch, b in channels:
        b = int(b)
        if b:
            v = (value >> np.uint64(shift)) & np.uint64((1 << b) - 1)
            if ch in "rgba":
                out[:, "rgba".index(ch)] = (v * np.uint64(255) // np.uint64((1 << b) - 1)).astype(np.uint8)
        shift += b
    return out.tobytes()


def flipRGBA32(data, width, height, horizontal, vertical):
    img = np.frombuffer(bytes(data[:width * height * 4]), dtype=np.uint8).reshape(height, width, 4)
    if horizontal:
        img = img[:, ::-1]
    if vertical:
        img = img[::-1]
    return np.ascontiguousarray(img).tobytes()
