import cv2
import numpy as np
from numpy.linalg import inv

# Config variable(s)
storage_file = "cam02_param_ext.xml"
matrices = [
    "intrinsic",
    "rotation_vector",
    "rotation_matrix",
    "translation",
    "distortion",
    "points_2d",
    "points_3d",
    "reprojection_errors"
]

# Utility function
def print_point(p):
    for row in p:
        for val in row:
            print("%.f" %val, end=" ")

def print_point_simple(p):
    for val in p:
        print("%.f" %val, end=" "),

# Load data from persistent storage
dic = {}
data = cv2.FileStorage(storage_file, cv2.FILE_STORAGE_READ)
for m in matrices:
    dic[m] = data.getNode(m).mat()

# Prepare matrices
rotation_matrix = np.mat(dic["rotation_matrix"])
translation_vector = np.mat(dic["translation"])
intrinsic_matrix = np.mat(dic["intrinsic"])

# Extrinsic Parameters Matrix
translation_vector_transposed = np.transpose(translation_vector)
extrinsic_matrix = np.concatenate((rotation_matrix, translation_vector_transposed), axis=1)

# Projection Matrix
projection_matrix = intrinsic_matrix * extrinsic_matrix

# Homography Matrix
p11 = projection_matrix[0,0]
p12 = projection_matrix[0,1]
p14 = projection_matrix[0,3]
p21 = projection_matrix[1,0]
p22 = projection_matrix[1,1]
p24 = projection_matrix[1,3]
p31 = projection_matrix[2,0]
p32 = projection_matrix[2,1]
p34 = projection_matrix[2,3]
homography_matrix = np.array([[p11,p12,p14], [p21,p22,p24], [p31,p32,p34]], dtype=np.float)
homography_matrix_inverse = inv(homography_matrix)

for i in range(0,10):

    # Prepare points
    np.set_printoptions(suppress=True)
    point_2D = np.append(np.array(dic["points_2d"][i]), np.array([[1]]), axis=1)
    print("\nPoint2D:", end=" ")
    print_point(point_2D)
    point_3d_expected = dic["points_3d"][i]
    print("\nPoint3D Exptected:", end=" ")
    print_point_simple(point_3d_expected)

    # Projection
    point_3D_w = np.mat(homography_matrix_inverse) * np.mat(np.transpose(point_2D))

    # Normalization
    point_3D = np.divide(point_3D_w,point_3D_w[2])
    point_3D[2] = 0

    # Show Result
    print("\nPoint3D:", end=" ")
    print_point(point_3D)
    print('')