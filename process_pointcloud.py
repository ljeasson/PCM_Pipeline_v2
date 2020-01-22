#!/usr/bin/python

import os
import glob
import sys, getopt

from segment_pointcloud import segment_point_cloud
from create_heightmap import create_heightmap_v2
from merge_tiles import merge_tiles

def main(argv):
    #print('Number of arguments:', len(sys.argv), 'arguments.')
    #print('Argument List:', str(sys.argv))
    
    directory = ''

    try:
        opts, args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        print('USAGE: process_pointcloud.py -i <input file or directory>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print('USAGE: process_pointcloud.py -i <input file or directory>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            directory = arg

    # If input ends with .laz
    if directory.endswith(".laz"):
        print('Incorrect file format\nUse .las or .laz point clouds')
        sys.exit()
    
    print('Input: ', directory, '\n')

    # IF INPUT IS A POINT CLOUD
    if directory.endswith(".las"):
        # Get point cloud file name without ".las"
        directory_no_ext = directory[ : directory.index(".")]

        # Segment Point Cloud into vegetation and ground
        segment_point_cloud(directory, directory_no_ext)
    
    # IF INPUT IS A DIRECTORY
    else:
        # Merge directory of tiles
        merge_tiles(directory, 0.5)

        merged_directory = ""

        for dirpath,_,filenames in os.walk(directory+"\merged"):
            for f in filenames:
                print(f)
                merged_directory = os.path.abspath(os.path.join(dirpath, f))
        
        merged_directory_no_ext = merged_directory[: merged_directory.index(".")]

        print("merged_directory:",merged_directory)
        print("merged_directory_no_ext",merged_directory_no_ext)
        print()

        # Segment Point Clouds into vegetation and ground
        segment_point_cloud(merged_directory, merged_directory_no_ext)
    
    # Get point clouds
    base_point_cloud, ground_point_cloud, veg_point_cloud, veg_point_cloud_subsampled = "",[],[],[]
    base_point_cloud_txt, ground_point_cloud_txt, veg_point_cloud_txt, building_point_cloud_txt = "","","",""
    for file in os.listdir(os.listdir(directory+"\merged")):
        if file.endswith(".las"):
            if "_ground.las" in file: ground_point_cloud.append(file)
            elif "_vegetation.las" in file: veg_point_cloud.append(file)
            elif "_vegetation_subsampled" in file: veg_point_cloud_subsampled.append(file)
            else: base_point_cloud = file
        if file.endswith(".txt"):
            if "_ground.txt" in file: ground_point_cloud_txt = file
            elif "_vegetation.txt" in file: veg_point_cloud_txt = file
            elif "_building.txt" in file: building_point_cloud_txt = file
            else: base_point_cloud_txt = file

    print(base_point_cloud, base_point_cloud_txt)
    print(ground_point_cloud, ground_point_cloud_txt)
    print(veg_point_cloud, veg_point_cloud_txt, veg_point_cloud_subsampled)
    print(building_point_cloud_txt)

    # Create heightmap from Ground point cloud
    #fileName_ground = input_point_cloud[:input_point_cloud.index(".")]
    #create_heightmap(ground_point_cloud, fileName_ground)
    
    # Open UE4 Editor with PCM Pipeline
    print("OPENING UE4 EDITOR WITH PCM PIPELINE")
    #os.system("UE4Editor 'D:\Users\Lee\Unreal Projects\PCM_PIpeline_v2\PCM_PIpeline_v2.uproject'")
    print("DONE\n")


if __name__ == "__main__":
    main(sys.argv[1:])