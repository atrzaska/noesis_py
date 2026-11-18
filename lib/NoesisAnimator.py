import numpy as np
import noesis
import rapi

# Skeleton + animation playback for the viewer.
#
# The engine applies a NoeMat43 to a point as Math_TransformPointByMatrix does:
# p'[r] = dot(m[r], p) + m[3][r] (and NoeMat43 a * b applies a first, then b). Here
# matrices are kept as 4x4 row-vector matrices, p' = p * M with M = [[m[0..2]^T, 0], [m[3], 1]],
# so world = local * parentWorld. Bone matrices given to setBones are model-space (world)
# bind poses; animation keys are local (parent-space) transforms. Keyframe quaternions are
# therefore the conjugate of the textbook (x, y, z, w) of a rotation, as in real Noesis
# (Rich's fmt_ue4.py converts with NoeQuat((-x, -y, -z, w))).


def mat43ToNp(m):
    out = np.identity(4)
    for r in range(3):
        out[:3, r] = (m[r][0], m[r][1], m[r][2])
    out[3, :3] = (m[3][0], m[3][1], m[3][2])
    return out


def quatToNp(q):
    # noesis.quatToMat43(q) (transposed = 0), as a row-vector rotation.
    x, y, z, w = q[0], q[1], q[2], q[3]
    xx, yy, zz = x * x, y * y, z * z
    xy, xz, yz = x * y, x * z, y * z
    wx, wy, wz = w * x, w * y, w * z
    return np.array([
        (1.0 - 2.0 * (yy + zz), 2.0 * (xy + wz), 2.0 * (xz - wy)),
        (2.0 * (xy - wz), 1.0 - 2.0 * (xx + zz), 2.0 * (yz + wx)),
        (2.0 * (xz + wy), 2.0 * (yz - wx), 1.0 - 2.0 * (xx + yy)),
    ]).T


def nlerp(a, b, t):
    if np.dot(a, b) < 0.0:
        b = -b
    q = a + (b - a) * t
    n = np.linalg.norm(q)
    return q / n if n > 0 else a


class Track:
    """One keyed channel: times (anim units) and values (n, k)."""

    def __init__(self, keys, width):
        self.times = np.array([float(k.time) for k in keys])
        self.values = np.array([[float(v) for v in k.value[:width]] if width > 1 else [float(k.value)]
                                for k in keys])
        self.nearest = False

    def sample(self, t, quat=False):
        times = self.times
        if len(times) == 1 or t <= times[0]:
            return self.values[0]
        if t >= times[-1]:
            return self.values[-1]
        i = int(np.searchsorted(times, t, side="right")) - 1
        a, b = self.values[i], self.values[i + 1]
        if self.nearest:
            return a
        f = (t - times[i]) / (times[i + 1] - times[i])
        return nlerp(a, b, f) if quat else a + (b - a) * f


class Skeleton:
    def __init__(self, bones):
        self.bones = bones
        self.count = len(bones)
        byIndex = {b.index: i for i, b in enumerate(bones)}
        byName = {b.name: i for i, b in enumerate(bones)}
        self.parents = []
        for b in bones:
            p = -1
            if b.parentName is not None and b.parentName in byName:
                p = byName[b.parentName]
            elif b.parentIndex is not None and b.parentIndex >= 0 and b.parentIndex in byIndex:
                p = byIndex[b.parentIndex]
            self.parents.append(p)
        self.byIndex = byIndex
        self.bind = np.array([mat43ToNp(b.getMatrix()) for b in bones])
        self.invBind = np.linalg.inv(self.bind)
        # parents-first evaluation order
        order, seen = [], set()

        def place(i):
            if i in seen:
                return
            seen.add(i)
            if self.parents[i] >= 0:
                place(self.parents[i])
            order.append(i)
        for i in range(self.count):
            place(i)
        self.order = order
        self.bindLocal = np.empty_like(self.bind)
        for i in range(self.count):
            p = self.parents[i]
            self.bindLocal[i] = self.bind[i] @ self.invBind[p] if p >= 0 else self.bind[i]

    def world(self, local):
        w = np.empty_like(local)
        for i in self.order:
            p = self.parents[i]
            w[i] = local[i] @ w[p] if p >= 0 else local[i]
        return w

    def skinMatrices(self, local):
        """Per-bone skinning matrices (row-vector): v' = v * invBind * world."""
        return self.invBind @ self.world(local)


class KeyFramedAnim:
    def __init__(self, skeleton, anim):
        self.name = anim.name
        self.skeleton = skeleton
        self.frameRate = float(anim.frameRate) or 20.0
        self.channels = []
        end = 0.0
        for kb in anim.kfBones:
            if kb.boneIndex not in skeleton.byIndex:
                continue
            i = skeleton.byIndex[kb.boneIndex]
            rot = Track(kb.rotationKeys, 4) if kb.rotationKeys else None
            pos = Track(kb.translationKeys, 3) if kb.translationKeys else None
            scl = None
            if kb.scaleKeys:
                width = 3 if kb.scaleType in (noesis.NOEKF_SCALE_VECTOR_3, noesis.NOEKF_SCALE_TRANSPOSED_VECTOR_3) else 1
                scl = Track(kb.scaleKeys, width)
            for track, interp in ((rot, kb.rotationInterpolation), (pos, kb.translationInterpolation),
                                  (scl, kb.scaleInterpolation)):
                if track is not None:
                    track.nearest = interp == noesis.NOEKF_INTERPOLATE_NEAREST
                    end = max(end, track.times[-1])
            self.channels.append((i, rot, pos, scl))
        # Key times are in seconds at frameRate frames per second.
        self.numFrames = int(round(end * self.frameRate)) + 1

    def local(self, frame):
        local = self.skeleton.bindLocal.copy()
        t = frame / self.frameRate
        for i, rot, pos, scl in self.channels:
            m = local[i]
            if rot is not None:
                r = quatToNp(rot.sample(t, quat=True))
            else:
                r = m[:3, :3].copy()
            if scl is not None:
                s = scl.sample(t)
                r = r * (s[:, None] if len(s) == 3 else s[0])
            m[:3, :3] = r
            if pos is not None:
                m[3, :3] = pos.sample(t)
        return local


class FrameMatAnim:
    """NoeAnim: flat list of local NoeMat43, frame-major."""

    def __init__(self, skeleton, anim):
        self.name = anim.name
        self.skeleton = skeleton
        self.frameRate = float(anim.frameRate) or 20.0
        self.numFrames = anim.numFrames
        n = len(anim.bones)
        mats = np.array([mat43ToNp(m) for m in anim.frameMats])
        self.mats = mats.reshape(self.numFrames, n, 4, 4) if n else mats
        self.map = [skeleton.byIndex.get(b.index, -1) for b in anim.bones]

    def local(self, frame):
        f = min(int(frame), self.numFrames - 1)
        local = self.skeleton.bindLocal.copy()
        for j, i in enumerate(self.map):
            if i >= 0:
                local[i] = self.mats[f, j]
        return local


class Animator:
    """Plays a model's animations; speed from setPreviewOption("setAnimSpeed")."""

    def __init__(self, model):
        self.skeleton = Skeleton(model.bones) if getattr(model, "bones", None) else None
        self.anims = []
        if self.skeleton:
            for anim in getattr(model, "anims", None) or []:
                if hasattr(anim, "kfBones"):
                    self.anims.append(KeyFramedAnim(self.skeleton, anim))
                elif hasattr(anim, "frameMats"):
                    self.anims.append(FrameMatAnim(self.skeleton, anim))
        self.current = 0
        self.frame = 0.0
        self.playing = True
        self.bindPose = False
        speed = rapi.getPreviewOption("setAnimSpeed") if hasattr(rapi, "getPreviewOption") else None
        self.speed = float(speed) if speed else None
        self._cache = (None, None)

    @property
    def anim(self):
        return self.anims[self.current] if self.anims else None

    def fps(self):
        return self.speed or (self.anim.frameRate if self.anim else 30.0)

    def advance(self, seconds):
        anim = self.anim
        if not anim or not self.playing:
            return
        self.frame = (self.frame + seconds * self.fps()) % max(1, anim.numFrames)

    def step(self, frames):
        anim = self.anim
        if anim:
            self.frame = (self.frame + frames) % max(1, anim.numFrames)

    def next(self, delta=1):
        if self.anims:
            self.current = (self.current + delta) % len(self.anims)
            self.frame = 0.0

    def skinMatrices(self):
        """(bones, 4, 4) skinning matrices for the current frame, or None (bind pose)."""
        anim = self.anim
        if not anim or self.bindPose:
            return None
        key = (self.current, int(self.frame))
        if self._cache[0] != key:
            self._cache = (key, self.skeleton.skinMatrices(anim.local(int(self.frame))))
        return self._cache[1]
