import numpy as np

def dodecahedron():
    a = 2 / 3                    # 0.666
    b = (5 / 9)**0.5             # 0.745
    c = (1 / 3)**0.5             # 0.577
    d = 1 / 3                    # 0.333
    e = (3 + 5**0.5) / 6         # 0.872
    f = ((3 - 5**0.5) / 6)**0.5  # 0.356
    g = (3 - 5**0.5) / 6         # 0.127
    h = ((3 + 5**0.5) / 6)**0.5  # 0.934
    pts = np.array(
      [[ 0,  0,  1],
       [ a,  0,  b],
       [-d,  c,  b],
       [-d, -c,  b],
       [ b,  c,  d],
       [ b, -c,  d],
       [-e,  f,  d],
       [ g,  h,  d],
       [ g, -h,  d],
       [-e, -f,  d],
       [ e,  f, -d],
       [ e, -f, -d],
       [-b,  c, -d],
       [-g,  h, -d],
       [-g, -h, -d],
       [-b, -c, -d],
       [ d,  c, -b],
       [ d, -c, -b],
       [-a,  0, -b],
       [ 0,  0, -1]], dtype=np.float)
    faces = np.array( 
      [[ 0,  1,  4,  7,  2],
       [ 0,  2,  6,  9,  3],
       [ 0,  3,  8,  5,  1],
       [ 1,  5, 11, 10,  4],
       [ 2,  7, 13, 12,  6],
       [ 3,  9, 15, 14,  8],
       [ 4, 10, 16, 13,  7],
       [ 5,  8, 14, 17, 11],
       [ 6, 12, 18, 15,  9],
       [10, 11, 17, 19, 16],
       [12, 13, 16, 19, 18],
       [14, 15, 18, 19, 17]], dtype=np.uint32)
    return pts, faces

def pentadodecahedron():
    pts, faces = dodecahedron()
    fc = [np.mean(pts[f, :], axis=0) for f in faces]
    pts = np.vstack((pts, fc))
    pts /= np.linalg.norm(pts, axis=1).reshape(-1, 1)
    tri = []
    for i in range(12):
        for j in range(5):
            tri.append([20 + i, faces[i][j], faces[i][(j + 1) % 5]])
    tri = np.array(tri, dtype=np.uint32)
    return pts, tri

def normalize(r):
    return r / np.linalg.norm(r)

def subdivide(pts, tri):
    tri = np.hstack((tri, tri[:, :1]))
    edges = zip(tri[:, :-1].flatten(), tri[:, 1:].flatten())
    edges = [(a, b) for a, b in edges if a < b]
    newpts = {}
    pts = list(pts)
    for v1, v2 in edges:
        newpts[(v1, v2)] = len(pts)
        pts.append(normalize(0.5 * (pts[v1] + pts[v2])))
    newtri = []
    for v1, v2, v3, _ in tri:
        v12 = newpts[tuple(sorted((v1, v2)))]
        v23 = newpts[tuple(sorted((v2, v3)))]
        v31 = newpts[tuple(sorted((v3, v1)))]
        newtri.append((v1, v12, v31))
        newtri.append((v12, v2, v23))
        newtri.append((v12, v23, v31))
        newtri.append((v31, v23, v3))
    return np.array(pts), np.array(newtri, dtype=np.uint32)

def icosphere(levels=0):
    filename = 'icosph.%d.npz' % levels
    try:  # Trying to load cached
        loaded = np.load(filename)
        pts = loaded['pts']
        tri = loaded['tri']
        return pts, tri
    except:
        pass

    pts, tri = pentadodecahedron()
    for _ in range(levels):
        pts, tri = subdivide(pts, tri)
    pts = pts.astype(np.float32)
    np.savez_compressed(filename, pts=pts, tri=tri)

    return pts, tri
