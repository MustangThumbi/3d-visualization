
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure


# Load the segmentation file
label_train00 = np.load('label_train00.npy')

# Compute vertex coordinates in mm and triangles for representing the segmentation boundary
verts, faces, normals, values = measure.marching_cubes_lewiner(
    label_train00, 0)

# Test three sagittal planes of your choice to divide this triangulated surface into two surfaces, left and right


def surface_dividing(verts, faces, sagittal_plane):
    left_verts = []
    left_faces = []
    right_verts = []
    right_faces = []
    for face in faces:
        v1 = verts[face[0]]
        v2 = verts[face[1]]
        v3 = verts[face[2]]
        if v1[0] < sagittal_plane and v2[0] < sagittal_plane and v3[0] < sagittal_plane:
            left_verts.append(v1)
            left_verts.append(v2)
            left_verts.append(v3)
            left_faces.append(face)
        elif v1[0] > sagittal_plane and v2[0] > sagittal_plane and v3[0] > sagittal_plane:
            right_verts.append(v1)
            right_verts.append(v2)
            right_verts.append(v3)
            right_faces.append(face)
        else:
            # Intersecting with one or two vertices
            if v1[0] == sagittal_plane or v2[0] == sagittal_plane or v3[0] == sagittal_plane:
                # Add the vertex to both left and right
                left_verts.append(v1)
                left_verts.append(v2)
                left_verts.append(v3)
                right_verts.append(v1)
                right_verts.append(v2)
                right_verts.append(v3)
                # Add the face to both left and right
                left_faces.append(face)
                right_faces.append(face)
            # Intersecting with two edges
            else:
                # Find the two intersecting edges
                if v1[0] < sagittal_plane and v2[0] > sagittal_plane:
                    edge1 = [v1, v2]
                    if v3[0] < sagittal_plane:
                        edge2 = [v3, v1]
                    else:
                        edge2 = [v2, v3]
                elif v2[0] < sagittal_plane and v3[0] > sagittal_plane:
                    edge1 = [v2, v3]
                    if v1[0] < sagittal_plane:
                        edge2 = [v1, v2]
                    else:
                        edge2 = [v3, v1]
                elif v3[0] < sagittal_plane and v1[0] > sagittal_plane:
                    edge1 = [v3, v1]
                    if v2[0] < sagittal_plane:
                        edge2 = [v2, v3]
                    else:
                        edge2 = [v1, v2]
                # Compute the intersection point
                x1, y1, z1 = edge1[0]
                x2, y2, z2 = edge1[1]
                x3, y3, z3 = edge2[0]
                x4, y4, z4 = edge2[1]
                x = (sagittal_plane*(z1*(x2-x3)+x1*(z3-z2)+x3*z2-x2*z3)
                     + (y1*(z2-z3)+z1*(y3-y2)+y2*z3-y3*z2)*(x4-x3)
                     + (x1*(y2-y3)+y1*(x3-x2)+x2*y3-x3*y2)*(z4-z3)) / ((x2-x1)*(z4-z3)+(y2-y1)*(x4-x3)+(z2-z1)*(y4-y3))
                y = (sagittal_plane*(z1*(y2-y3)+y1*(z3-z2)+y3*z2-y2*z3)
                     + (x1*(y3-y2)+y1*(x2-x3)+x3*y2-x2*y3)*(z4-z3)
                     + (y1*(x3-x2)+x1*(y2-y3)+x2*y3-x3*y2)*(x4-x3)) / ((x2-x1)*(z4-z3)+(y2-y1)*(x4-x3)+(z2-z1)*(y4-y3))
                z = (sagittal_plane*(x1*(y2-y3)+y1*(x3-x2)+x2*y3-x3*y2)
                     + (x1*(z3-z2)+z1*(x2-x3)+x3*z2-x2*z3)*(y4-y3)
                     + (z1*(x3-x2)+x1*(z2-z3)+x2*z3-x3*z2)*(x4-x3)) / ((x2-x1)*(z4-z3)+(y2-y1)*(x4-x3)+(z2-z1)*(y4-y3))
                # Add the intersection point to both left and right
                left_verts.append([x, y, z])
                right_verts.append([x, y, z])
                # Add the two new faces to both left and right
                left_faces.append([face[0], face[1], len(left_verts)-1])
                left_faces.append([face[1], face[2], len(left_verts)-1])
                right_faces.append([face[0], face[1], len(right_verts)-1])
                right_faces.append([face[1], face[2], len(right_verts)-1])
    return left_verts, left_faces, right_verts, right_faces

# Plot these 6 divided surfaces in a clear and visually comparable manner


def plot_surface(verts, faces, title):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x, y, z = zip(*verts)
    ax.plot_trisurf(x, y, faces, z, cmap='Spectral')
    ax.set_title(title)
    plt.show()


# Plot the original surface
plot_surface(verts, faces, 'Original Surface')
