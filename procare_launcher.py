# ----------------------------------------------------------------------------
# <                               ProCare                                    >
# ----------------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2020 Merveille Eguida
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
# ----------------------------------------------------------------------------
#
#
########################## OPEN3D ORIGINAL WORK ##############################
# ----------------------------------------------------------------------------
# -                        Open3D: www.open3d.org                            -
# ----------------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2018 www.open3d.org
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.




def process_pointcloud(pointcloud_, radius_normal_, 
        radius_feature_, max_nn_normal_, max_nn_feature_):

    """This fuction estimates normals and calculate 
    the fast point feature histogramm"""

    estimate_normals(pointcloud_, KDTreeSearchParamHybrid(
               radius=radius_normal_, max_nn=max_nn_normal_)) 
    cfpfh = compute_cfpfh_feature(pointcloud_, KDTreeSearchParamHybrid(
               radius=radius_feature_, max_nn=max_nn_feature_))
    return cfpfh, pointcloud_



def global_registration(source_, target_, cfpfh_source_, cfpfh_target_, 
        distance_threshold_, transformation_type_, n_ransac_, 
        similarity_threshold_, max_iter_, max_valid_):

    """Initial RANSAC alignement based of features"""

    function_transtype = FUNCTIONS[transformation_type_]
    # default TransformationEstimationPointToPoint: with_scaling = False
    result = registration_ransac_based_on_feature_matching(source_, target_,
        cfpfh_source_, cfpfh_target_,
        max_correspondence_distance=distance_threshold_,
        estimation_method=function_transtype(), ransac_n=n_ransac_,
        checkers=[CorrespondenceCheckerBasedOnEdgeLength(similarity_threshold_),
        CorrespondenceCheckerBasedOnDistance(distance_threshold_)],
        criteria=RANSACConvergenceCriteria(max_iter_, max_valid_))
    return result 



def fine_registration(source_, target_, result_ransac_, distance_threshold_, 
        transformation_type_, relative_rmse_, relative_fitness_, max_iter_):
    
    function_transtype = FUNCTIONS[transformation_type_]
    # default TransformationEstimationPointToPoint: with_scaling = False
    result = registration_icp(source_, target_,
        max_correspondence_distance=distance_threshold_,
        init=result_ransac_.transformation,
        estimation_method=function_transtype(),
        criteria=ICPConvergenceCriteria(relative_fitness_, relative_rmse_, max_iter_))
    return result



if __name__ == '__main__':
  
    import os
    import argparse
    import copy

    from procare.open3d.open3d.registration import registration_icp
    from procare.open3d.open3d.registration import registration_ransac_based_on_feature_matching
    from procare.open3d.open3d.geometry import read_point_cloud
    from procare.open3d.open3d.registration import compute_cfpfh_feature
    from procare.open3d.open3d.geometry import estimate_normals
    from procare.open3d.open3d.geometry import KDTreeSearchParamHybrid
    from procare.open3d.open3d.registration import CorrespondenceCheckerBasedOnEdgeLength
    from procare.open3d.open3d.registration import CorrespondenceCheckerBasedOnDistance
    from procare.open3d.open3d.registration import RANSACConvergenceCriteria
    from procare.open3d.open3d.registration import ICPConvergenceCriteria
    from procare.open3d.open3d.registration import TransformationEstimationPointToPoint
    from procare.open3d.open3d.registration import TransformationEstimationPointToPlane

    from procare.convert import _volsite_cavity_
    from procare.procarescores import _ph4_ext_

    import numpy as np


    parser = argparse.ArgumentParser(description='Parameters for ProCare')

    # ransac
    parser.add_argument('-rv', '--ransacvalid', type=int, 
        help='RANCAC convergence criteria: maximum validation', 
        required=False,
        default=500)

    parser.add_argument('-ri', '--ransaciter', type=int,
        help='RANCAC convergence criteria: maximum iteration', 
        required=False,
        default=4000000)

    parser.add_argument('-rn', '--ransacn', type=int,
        help='RANSAC: number of pairs to validate at each iteration', 
        required=False,
        default=4)

    # global registration
    parser.add_argument('-gt', '--globaltranstype', type=str,
        help='Transformation estimation type for global registration', 
        required=False,
        default='TransformationEstimationPointToPoint')

    parser.add_argument('-gd', '--globaldist', type=float,
        help='Distance threshold for correspondences set in global registration', 
        required=False,
        default=1.5)

    # checker
    parser.add_argument('-cs', '--checkersim', type=float, 
        help='Checker similarity threshold: between 0 and 1', 
        required=False,
        default=0.9)

    # icp
    parser.add_argument('-it', '--icptranstype', type=str,
        help='Transformation estimation type for ICP registration', 
        required=False,
        default='TransformationEstimationPointToPoint')

    parser.add_argument('-id', '--icpdist', type=float,
        help='Distance threshold for correspondences set in ICP registration', 
        required=False,
        default=3)

    parser.add_argument('-ir', '--icprmse', type=float,
        help='RMSE relative threshold for ICP terminaison', # default observed as acceptable
        required=False,
        default=10e-6)

    parser.add_argument('-if', '--icpfitness',type=float,
        help='Fitness relative threshold for ICP terminaison', 
        required=False,
        default=10e-6)

    parser.add_argument('-ii', '--icpiter', type=int,
        help='ICP convergence criteria: maximum iteration', 
        required=False,
        default=100)

    # normals
    parser.add_argument('-nr', '--normalrad', type=float,
        help='Radius for local surface normal estimation on a point', 
        required=False,
        default=3.1)

    parser.add_argument('-nm', '--normalmaxn', type=int,
        help=('Maximum number of neighbors to consider for local surface normal '
              'estimation on a point'), 
        required=False,
        default=471)

    # features
    parser.add_argument('-fr', '--featurerad', type=float,
        help='Radius for local surface feature estimation on a point', 
        required=False,
        default=3.1)

    parser.add_argument('-fm', '--featuremaxn', type=int,
        help=('Maximum number of neighbors to consider for local surface feature '
              'estimation on a point'), 
        required=False,
        default=135)

    # output
    parser.add_argument('-o', '--output', type=str,
        help='Complete output file', 
        required=False,
        default='procare.tsv')

    parser.add_argument('-so', '--scoreoutput', type=str,
        help='Simplifiled output file: scores', 
        required=False,
        default='procare_scores.tsv')

    parser.add_argument('-p', '--paramid', type=str,
        help='ID for parameters identification', 
        required=False,
        default='default')

    parser.add_argument('-c', '--classification', type=str,
        help='Class for retrospective screening: 0 or 1',
        choices=['0', '1'],
        required=False,
        default='NAN')

    parser.add_argument('--transform', action='store_true',
        help='output rotated mol2', 
        required=False)

    # inputs
    parser.add_argument('-s', '--source', type=str,
        help='Source mol2 file', 
        required=True)

    parser.add_argument('-t', '--target', type=str,
        help='Target mol2 file', 
        required=True)

    args = parser.parse_args()


    FUNCTIONS = {
    'TransformationEstimationPointToPlane': TransformationEstimationPointToPlane,
    'TransformationEstimationPointToPoint': TransformationEstimationPointToPoint 
    #default: TransformationEstimationPointToPoint(with_scaling = False)
    }


    source_cavity = _volsite_cavity_()
    sourfe_file, source_prop, source_color = source_cavity.mol2_to_pcd(args.source)
    target_cavity = _volsite_cavity_()
    target_file, target_prop, target_color = target_cavity.mol2_to_pcd(args.target)

    if sourfe_file and target_file != -1:
        source = read_point_cloud(sourfe_file)
        target = read_point_cloud(target_file)

        source_cfpfh, source = process_pointcloud(pointcloud_=source,
                                             radius_normal_=args.normalrad,
                                             radius_feature_=args.featurerad,
                                             max_nn_normal_=args.normalmaxn,
                                         max_nn_feature_=args.featuremaxn)

        target_cfpfh, target = process_pointcloud(pointcloud_=target,
                                         radius_normal_=args.normalrad,
                                         radius_feature_=args.featurerad,
                                         max_nn_normal_=args.normalmaxn,
                                         max_nn_feature_=args.featuremaxn)


        result_global = global_registration(source_=source,
                                            target_=target,
                                            cfpfh_source_=source_cfpfh,
                                            cfpfh_target_=target_cfpfh,
                                            distance_threshold_=args.globaldist,
                                            transformation_type_=args.globaltranstype,
                                            n_ransac_=args.ransacn,
                                            similarity_threshold_=args.checkersim,
                                            max_iter_=args.ransaciter,
                                            max_valid_=args.ransacvalid)

        result_fine = fine_registration(source_=source,
                                        target_=target,
                                        result_ransac_=result_global,
                                        distance_threshold_=args.icpdist,
                                        transformation_type_=args.icptranstype,
                                        relative_rmse_=args.icprmse,
                                        relative_fitness_=args.icpfitness,
                                        max_iter_=args.icpiter)

        source_transformed = copy.deepcopy(source)
        source_transformed.transform(result_fine.transformation)
        print(source_transformed)

        

        if args.transform:
            rot_file = 'rot_{}.mol2'.format(os.path.splitext(sourfe_file)[0])
            rotated_mol2 = _volsite_cavity_()
            rot_coords = []
            for point, color in zip(source_transformed.points, 
                                    source_color):
                rot_coords.append([point[0], point[1], point[2], color])

            rotated_mol2.write_mol2(rot_file, rot_coords)

        
        ph4_ext = _ph4_ext_(source_transformed.points, target.points, 
                                            source_prop, target_prop, 1.5)

        ratio_aligned, ratio_CA_in_aligned, \
            ratio_CZ_in_aligned, ratio_N_in_aligned, \
            ratio_NZ_in_aligned, ratio_O_in_aligned, \
            ratio_OD1_in_aligned, ratio_OG_in_aligned, \
            ratio_DU_in_aligned = ph4_ext.get_similarity_by_rules()

        score = ph4_ext.tversky_similarity()

        if not os.path.isfile(args.scoreoutput):
            with open(args.scoreoutput, "w") as of:
                of.write("Source\tTarget\tScore\n")

        with open(args.scoreoutput, 'a') as of:
            of.write("{}\t{}\t{}\n".format(os.path.splitext(sourfe_file)[0],
                                           os.path.splitext(target_file)[0],
                                           score))


        if not os.path.isfile(args.output):
            with open(args.output, "w") as of:
                of.write("Param_id\tSource\tTarget\tClass\tScore\t"

                         "CA_contrib\tCZ_contrib\tO_contrib\tN_contrib\t"
                         "OD1_contrib\tOG_contrib\tNZ_contrib\tDU_contrib\t"

                         "G_fitness\tG_RMSE\tICP_fitness\tICP_RMSE\t"

                         "G_11\tG_12\tG_13\tG_14\t"
                         "G_21\tG_22\tG_23\tG_24\t"
                         "G_31\tG_32\tG_33\tG_34\t"
                         "G_41\tG_42\tG_43\tG_44\t"

                         "ICP_11\tICP_12\tICP_13\tICP_14\t"
                         "ICP_21\tICP_22\tICP_23\tICP_24\t"
                         "ICP_31\tICP_32\tICP_33\tICP_34\t"
                         "ICP_41\tICP_42\tICP_43\tICP_44\n")

        with open(args.output, 'a') as of:
            of.write(("{}\t{}\t{}\t{}\t{}\t"
                      "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t"
                      "{}\t{}\t{}\t{}\t"
                      "{}\t{}\t{}\t{}\t"
                      "{}\t{}\t{}\t{}\t"
                      "{}\t{}\t{}\t{}\t"
                      "{}\t{}\t{}\t{}\t"
                      "{}\t{}\t{}\t{}\t"
                      "{}\t{}\t{}\t{}\t"
                      "{}\t{}\t{}\t{}\t"
                      "{}\t{}\t{}\t{}\n"
                      ).format(args.paramid,
                               os.path.splitext(sourfe_file)[0],
                               os.path.splitext(target_file)[0],
                               args.classification,
                               score,
                               ratio_CA_in_aligned,
                               ratio_CZ_in_aligned,
                               ratio_O_in_aligned,
                               ratio_N_in_aligned,
                               ratio_OD1_in_aligned,
                               ratio_OG_in_aligned,
                               ratio_NZ_in_aligned,
                               ratio_DU_in_aligned,
                               result_global.fitness,
                               result_global.inlier_rmse,
                               result_fine.fitness,
                               result_fine.inlier_rmse,
                               np.array(result_global.transformation)[0][0],
                               np.array(result_global.transformation)[0][1],
                               np.array(result_global.transformation)[0][2],
                               np.array(result_global.transformation)[0][3],
                               np.array(result_global.transformation)[1][0],
                               np.array(result_global.transformation)[1][1],
                               np.array(result_global.transformation)[1][2],
                               np.array(result_global.transformation)[1][3],
                               np.array(result_global.transformation)[2][0],
                               np.array(result_global.transformation)[2][1],
                               np.array(result_global.transformation)[2][2],
                               np.array(result_global.transformation)[2][3],
                               np.array(result_global.transformation)[3][0],
                               np.array(result_global.transformation)[3][1],
                               np.array(result_global.transformation)[3][2],
                               np.array(result_global.transformation)[3][3],
                               np.array(result_fine.transformation)[0][0],
                               np.array(result_fine.transformation)[0][1],
                               np.array(result_fine.transformation)[0][2],
                               np.array(result_fine.transformation)[0][3],
                               np.array(result_fine.transformation)[1][0],
                               np.array(result_fine.transformation)[1][1],
                               np.array(result_fine.transformation)[1][2],
                               np.array(result_fine.transformation)[1][3],
                               np.array(result_fine.transformation)[2][0],
                               np.array(result_fine.transformation)[2][1],
                               np.array(result_fine.transformation)[2][2],
                               np.array(result_fine.transformation)[2][3],
                               np.array(result_fine.transformation)[3][0],
                               np.array(result_fine.transformation)[3][1],
                               np.array(result_fine.transformation)[3][2],
                               np.array(result_fine.transformation)[3][3]
                               ))

        os.system('rm {} {}'.format(sourfe_file, target_file))



