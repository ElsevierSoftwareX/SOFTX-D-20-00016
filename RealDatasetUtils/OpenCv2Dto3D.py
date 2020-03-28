import cv2
import numpy as np

def Project(points, intrinsic, distortion):
    result = []
    tvec = np.array([3.16912168e+004, -1.31297791e+003, 8.73433125e+004])
    rvec = np.array([-4.56216574e-001, 1.76409543e+000, 2.05966163e+000])
    if len(points) > 0:
        result, _ = cv2.projectPoints(points, rvec, tvec,
                                    intrinsic, distortion)
    return np.squeeze(result, axis=1)


def Unproject(points, Z, intrinsic, distortion):
    f_x = intrinsic[0, 0]
    f_y = intrinsic[1, 1]
    c_x = intrinsic[0, 2]
    c_y = intrinsic[1, 2]
    # This was an error before
    # c_x = intrinsic[0, 3]
    # c_y = intrinsic[1, 3]

    # Step 1. Undistort.
    points_undistorted = np.array([])
    if len(points) > 0:
        points_undistorted = cv2.undistortPoints(np.expand_dims(points, axis=1), intrinsic, distortion, P=intrinsic)
    points_undistorted = np.squeeze(points_undistorted, axis=1)

    # Step 2. Reproject.
    result = []
    for idx in range(points_undistorted.shape[0]):
        z = Z[0] if len(Z) == 1 else Z[idx]
        x = (points_undistorted[idx, 0] - c_x) / f_x * z
        y = (points_undistorted[idx, 1] - c_y) / f_y * z
        result.append([x, y, z])
    return result






# https://stackoverflow.com/questions/14514357/converting-a-2d-image-point-to-a-3d-world-point
# NOT WORKING APPARENTLY (INVERTED X AND Y?)
def unproject_impl_1(point, intrinsic, distortion, tvec, rvec, rmatrix):
    
    tvec_n = -tvec
    #assert tvec_n[1] == -tvec[1]
    
    # Matricial product
    T = np.dot(rmatrix, tvec_n)
    d = np.dot(rmatrix, point)

    X = (T[2] / d[2]) * d[0] + T[0]
    Y = (T[2] / d[2]) * d[1] + T[1]

    return np.array([X, Y, 0.0])

    #Given 2D point   : [1440.20915769  222.29505995]
    #Expected 3D point: [    0. 34000.     0.]
    #Computed 3D point: [ 3.43124267e+04 -8.95367619e+04  0.00000000e+00]


    
# https://stackoverflow.com/questions/7836134/get-3d-coordinates-from-2d-image-pixel-if-extrinsic-and-intrinsic-parameters-are/10750648#10750648    
# NOT WORKING APPARENTLY
def unproject_impl_2(point, intrinsic, distortion, tvec, rvec, rmatrix):

    # H = K*[r1, r2, t],       //eqn 8.1, Hartley and Zisserman
    # with K being the camera intrinsic matrix, r1 and r2 being the first two columns of the rotation matrix, R; t is the translation vector.
    # Then normalize dividing everything by t3.

    submatrix = np.array([
        [rmatrix[0, 0], rmatrix[0, 1], tvec[0]],
        [rmatrix[1, 0], rmatrix[1, 1], tvec[1]],
        [rmatrix[2, 0], rmatrix[2, 1], tvec[2]],
    ])

    H_norm = np.dot(intrinsic, submatrix) / tvec[2]  # K*[r1, r2, t]

    projection = np.dot(H_norm, point)
    proj_norm = projection / point[2]

    return proj_norm



# https://stackoverflow.com/questions/12299870/computing-x-y-coordinate-3d-from-image-point
# BEST RESULT UP TO NOW: [ -845.03930096 34259.25073246     0.        ] -> Y MATCHES
def unproject_impl_3(point, intrinsic, distortion, tvec, rvec, rmatrix):

    r_inverse = np.linalg.inv(rmatrix)
    i_inverse = np.linalg.inv(intrinsic)

    #cv::Mat leftSideMat  = rotationMatrix.inv() * cameraMatrix.inv() * uvPoint;
    #cv::Mat rightSideMat = rotationMatrix.inv() * tvec;
    left_mat1 = np.dot(r_inverse, i_inverse)
    left_mat = np.dot(left_mat1, point)
    right_mat = np.dot(r_inverse, tvec)
    
    
    # double s = (285 + rightSideMat.at<double>(2,0))/leftSideMat.at<double>(2,0)); 
    s = (0 + right_mat[2]) / left_mat[2]; 
    # 0 represents the height Zconst

    #std::cout << "P = " << rotationMatrix.inv() * (s * cameraMatrix.inv() * uvPoint - tvec) << std::endl;
    result = np.dot(r_inverse, s * np.dot(i_inverse, point) - tvec)

    return result



# https://stackoverflow.com/questions/39394785/opencv-get-3d-coordinates-from-2d
def unproject_impl_4(point, intrinsic, distortion, tvec, rvec, rmatrix):

    # R^T
    rmatrix_t = [[rmatrix[j][i] for j in range(len(rmatrix))] for i in range(len(rmatrix[0]))]

    # -R^T
    rmatrix_t_negative = []
    for alist in rmatrix_t:
        newlist = [-x for x in alist]
        rmatrix_t_negative.append(newlist)

    # -R^T*t
    result = np.dot(rmatrix_t_negative, tvec)

    # [R^T|-R^T*t]
    final_matrix = np.c_[rmatrix_t, result]

    result = np.dot(final_matrix, np.r_[point, [1]])
    
    return result



# http://answers.opencv.org/question/38131/converting-a-2d-image-point-to-a-3d-world-point/
def unproject_impl_5(point, intrinsic, distortion, tvec, rvec, rmatrix):
    f_x = intrinsic[0, 0]
    f_y = intrinsic[1, 1]
    c_x = intrinsic[0, 2]
    c_y = intrinsic[1, 2]

    u = point[0]
    v = point[1]


    xt = (u/f_x) - (c_x/f_x)
    yt = (v/f_y) - (c_y/f_y)
    
    # K1 =      I have no idea on how to implement this 
    
    """
    float K1 = xt * rmatrix(2, 1) * worldY + xt * t3 - rmatrix(0,1) * worldY - t1
    float K2 = xt*r9 - r3
    float K3 = r1 - xt*r7


    float worldZ = (yt*r7*K1 + yt*K3*r8*worldY + yt*K3*t3 - r4*K1 - K3*r5*worldY - K3*t2)/
                    (r4*K2 + K3*r6 - yt*r7*K2 - yt*K3*r9);

    float worldX = (K1 + worldZ*K2)/K3;


    tmpPoint = Point3f(worldX, worldY, worldZ);
    """



def undistort_point(points, intrinsic, distortion):

    # Step 1. Undistort.
    points_undistorted = np.array([])
    if len(points) > 0:
        points_undistorted = cv2.undistortPoints(np.expand_dims(points, axis=1), intrinsic, distortion, P=intrinsic)
    points_undistorted = np.squeeze(points_undistorted, axis=1)


    pts = cv2.undistortPoints(np.expand_dims(points, axis=1), intrinsic, distortion)

    return np.r_[points_undistorted[0], [1]] #points_undistorted[0]



# https://stackoverflow.com/questions/51272055/opencv-unproject-2d-points-to-3d-with-known-depth-z
def main():
    # Intrinsic values
    #4.04310596e+003 0. 9.15485046e+002 0. 4.03170264e+003
    #4.26480865e+002 0. 0. 1.
    f_x = 4.04310596e+003
    f_y = 4.03170264e+003
    c_x = 9.15485046e+002
    c_y = 4.26480865e+002

    intrinsic = np.array([
        [f_x, 0.0, c_x],
        [0.0, f_y, c_y],
        [0.0, 0.0, 1.0]
    ])

    # Distorsion values: 4.86164242e-001 -3.57553625e+000 -1.77373271e-002 -3.11793620e-003
    distortion = np.array([4.86164242e-001, -3.57553625e+000, -1.77373271e-002, -3.11793620e-003])

    # traslation vector
    tvec = np.array([3.16912168e+004, -1.31297791e+003, 8.73433125e+004])
    # rotation vector
    rvec = np.array([-4.56216574e-001, 1.76409543e+000, 2.05966163e+000])
    # rotation matrix
    rmatrix = np.array([
        [-8.71332586e-001, -4.90659207e-001, 5.74691826e-003],
        [8.10814202e-002, -1.32417098e-001, 9.87872243e-001], 
        [-4.83947605e-001, 8.61231267e-001, 1.55162677e-001]
    ])
    
    # algorithm taken from here: 
    point_single = np.array([[0.0, 34000., 0.0],])
    point_single_projected = Project(point_single, intrinsic, distortion)
    Z = np.array([point[2] for point in point_single])
    point_single_unprojected = Unproject(point_single_projected,
                                        Z,
                                        intrinsic, distortion)


    # Here 1.0 is added to X, Y, as a value for Z
    point = np.array([1454.0, 223.0, 1.0])

    print("[GIVEN] 2D point:", point)
    print("[GIVEN] 3D point (expected):", point_single[0])
    print("[RESULT] 3D to 2D (projected):", point_single_projected[0])
    print("[RESULT] 3D Computed point:", point_single_unprojected[0])


    result = unproject_impl_1(point, intrinsic, distortion, tvec, rvec, rmatrix)
    print("[RESULT] 3D Computed point impl_1:", result)

    result = unproject_impl_2(point, intrinsic, distortion, tvec, rvec, rmatrix)
    print("[RESULT] 3D Computed point impl_2:", result)

    result = unproject_impl_3(point, intrinsic, distortion, tvec, rvec, rmatrix)
    print("[RESULT] 3D Computed point impl_3:", result)
    
    result = unproject_impl_4(point, intrinsic, distortion, tvec, rvec, rmatrix)
    print("[RESULT] 3D Computed point impl_4:", result)


    # Removing distortion to points
    point_single_projected = point = np.array([[1454.0, 223.0],])
    point = undistort_point(point_single_projected, intrinsic, distortion)

    result = unproject_impl_1(point, intrinsic, distortion, tvec, rvec, rmatrix)
    print("[RESULT] Undistorted 3D Computed point impl_1:", result)

    result = unproject_impl_2(point, intrinsic, distortion, tvec, rvec, rmatrix)
    print("[RESULT] Undistorted 3D Computed point impl_2:", result)

    result = unproject_impl_3(point, intrinsic, distortion, tvec, rvec, rmatrix)
    print("[RESULT] Undistorted 3D Computed point impl_3:", result)
    
    result = unproject_impl_4(point, intrinsic, distortion, tvec, rvec, rmatrix)
    print("[RESULT] Undistorted 3D Computed point impl_4:", result)

    

if __name__ == "__main__":
    main()