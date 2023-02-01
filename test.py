import matplotlib.pyplot as plt
from skimage import measure
import numpy as np


def surface_dividing(vertices, triangles, sagittal_plane):
    left_vertices = []
    right_vertices = []
    left_triangles = []
    right_triangles = []
    for vertex in vertices:
        if vertex[0] < sagittal_plane:
            left_vertices.append(vertex)
        else:
            right_vertices.append(vertex)
    for triangle in triangles:
        left_triangle = []
        right_triangle = []
        for vertex in triangle:
            if vertex[0] < sagittal_plane:
                left_triangle.append(vertex)
            else:
                right_triangle.append(vertex)
        if len(left_triangle) == 3:
            left_triangles.append(left_triangle)
        if len(right_triangle) == 3:
            right_triangles.append(right_triangle)
        if len(left_triangle) == 2 and len(right_triangle) == 1:
            # intersecting with one vertex
            left_triangles.append(left_triangle + right_triangle)
            right_triangles.append(right_triangle + left_triangle)
        if len(left_triangle) == 1 and len(right_triangle) == 2:
            # intersecting with one vertex
            left_triangles.append(left_triangle + right_triangle)
            right_triangles.append(right_triangle + left_triangle)
        if len(left_triangle) == 2 and len(right_triangle) == 2:
            # intersecting with two edges
            left_triangles.append(left_triangle + [right_triangle[0]])
            left_triangles.append([right_triangle[0]] + right_triangle)
            right_triangles.append(right_triangle + [left_triangle[0]])
            right_triangles.append([left_triangle[0]] + left_triangle)
    return left_vertices, left_triangles, right_vertices, right_triangles


# Load the segmentation file “label_train00.npy” file
label_train00 = np.load("label_train00.npy")
label_train00 = label_train00.astype(np.uint8)
label_train00 = np.transpose(label_train00, (2, 1, 0))

# Use skimage.measre.marching_cubes algorithm to compute vertex coordinates in mm

# triangles for representing the segmentation boundary argument is a string or a number
# representing the label of the object to be segmented
vertices, triangles, normals, values = measure.marching_cubes(
    label_train00, level=1, spacing=(1, 1, 1))


# Define three sagittal planes of your choice
sagittal_planes = [50, 100, 150]

# Compute the 6 divided surfaces
left_vertices, left_triangles, right_vertices, right_triangles = surface_dividing(
    vertices, triangles, sagittal_planes[0])
left_vertices2, left_triangles2, right_vertices2, right_triangles2 = surface_dividing(
    vertices, triangles, sagittal_planes[1])
left_vertices3, left_triangles3, right_vertices3, right_triangles3 = surface_dividing(
    vertices, triangles, sagittal_planes[2])

# Plot the 6 divided surfaces
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(left_vertices[:, 0], left_vertices[:, 1],
                left_vertices[:, 2], triangles=left_triangles, color='red')
ax.plot_trisurf(right_vertices[:, 0], right_vertices[:, 1],
                right_vertices[:, 2], triangles=right_triangles, color='blue')
ax.plot_trisurf(left_vertices2[:, 0], left_vertices2[:, 1],
                left_vertices2[:, 2], triangles=left_triangles2, color='red')
ax.plot_trisurf(right_vertices2[:, 0], right_vertices2[:, 1],
                right_vertices2[:, 2], triangles=right_triangles2, color='blue')
ax.plot_trisurf(left_vertices3[:, 0], left_vertices3[:, 1],
                left_vertices3[:, 2], triangles=left_triangles3, color='red')
ax.plot_trisurf(right_vertices3[:, 0], right_vertices3[:, 1],
                right_vertices3[:, 2], triangles=right_triangles3, color='blue')
plt.show()
