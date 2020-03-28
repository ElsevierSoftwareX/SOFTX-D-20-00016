import cv2
import numpy as np
from numpy.linalg import inv

# This script converts the "on screen" input file to 3D "pitch coordinates system" position.log file 

# Config variable(s)
storage_file = "cam01_param_ext.xml"
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

# I/O files
annotation_file = "positions_onscreen.log"
annotation_file_output = "positions_onthepitch.log"

# Utility function(s)
def print_point(p):
    for row in p:
        for val in row:
            print("%.f" % val, end=" ")


def print_point_simple(p):
    for val in p:
        print("%.f" % val, end=" "),


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
extrinsic_matrix = np.concatenate(
    (rotation_matrix, translation_vector_transposed), axis=1)

# Projection Matrix
projection_matrix = intrinsic_matrix * extrinsic_matrix

# Homography Matrix
p11 = projection_matrix[0, 0]
p12 = projection_matrix[0, 1]
p14 = projection_matrix[0, 3]
p21 = projection_matrix[1, 0]
p22 = projection_matrix[1, 1]
p24 = projection_matrix[1, 3]
p31 = projection_matrix[2, 0]
p32 = projection_matrix[2, 1]
p34 = projection_matrix[2, 3]
homography_matrix = np.array(
    [[p11, p12, p14], [p21, p22, p24], [p31, p32, p34]], dtype=np.float)
homography_matrix_inverse = inv(homography_matrix)


with open(annotation_file, "r") as annotation_file_pointer:
    with open(annotation_file_output, "w") as annotation_file_output_pointer:
        # Iterating over lines of the input file to convert each point into 3D point
        for line in annotation_file_pointer:

            # Get x and y parameter data
            parameter_list = line.split(' ')
            x = float(parameter_list[2])
            y = float(parameter_list[3])

            # Prepare points
            np.set_printoptions(suppress=True)
            point_2D = np.append(
                np.array([[x, y]]), np.array([[1]]), axis=1)
            #print("\nPoint2D:", end=" ")
            #print_point(point_2D)

            # Projection
            point_3D_w = np.mat(homography_matrix_inverse) * \
                np.mat(np.transpose(point_2D))

            # Normalization
            point_3D = np.divide(point_3D_w, point_3D_w[2])
            point_3D[2] = 0

            # Show Result
            #print("\nPoint3D:", end=" ")
            #print_point(point_3D)
            #print('')

            # Writing the point into output file
            line = "{0} {1} {2:.6f} {3:.6f}"
            print(line.format(parameter_list[0], parameter_list[1], float(point_3D[0]), float(point_3D[1])), file=annotation_file_output_pointer)


print("[PositionsLog 2d_to_3d] Done.")