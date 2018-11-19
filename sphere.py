import numpy as np

def sphere(n_phi, n_theta):
    pid = np.zeros((n_phi, n_theta), dtype=np.uint32)
    dtheta = np.pi / n_theta
    dphi = 2 * np.pi / n_phi
    theta = np.linspace(-np.pi / 2, np.pi / 2, n_theta + 1)
    phi = np.linspace(0, 2*np.pi, n_phi + 1)[:n_phi]
    k = 0
    pts = []
    for i in range(n_phi):
        for j in range(1, n_theta):
            r = [np.cos(theta[j]) * np.cos(phi[i]),
                 np.cos(theta[j]) * np.sin(phi[i]),
                 np.sin(theta[j])]
            pts.append(r)
            pid[i, j] = k
            k += 1
    nmid = len(pts)
    pts.append([0, 0, 1])
    pts.append([0, 0, -1])
    tri = []
    for i in range(n_phi):
        tri.append([nmid + 1, pid[(i+1) % n_phi, 1], pid[i, 1]])
        tri.append([nmid, pid[i, n_theta-1], pid[(i+1) % n_phi, n_theta-1]])
    for j in range(1, n_theta-1):
        for i in range(n_phi):
            i1 = (i+1) % n_phi
            p1 = pid[i, j]
            p2 = pid[i1, j]
            p3 = pid[i, j+1]
            p4 = pid[i1, j+1]
            tri.append([p1, p2, p3])
            tri.append([p2, p4, p3])
        
    return np.array(pts, dtype=np.float32), np.array(tri, dtype=np.uint32)
