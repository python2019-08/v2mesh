# 1. InterfaceCOLMAP -h

```sh
3rd/openMVS/make02/bin$ ./InterfaceCOLMAP -h
22:56:52 [App     ] OpenMVS x64 v2.4.0
22:56:52 [App     ] Build date: Feb 22 2026, 20:37:13
22:56:52 [App     ] CPU: Intel(R) Core(TM) i9-10900K CPU @ 3.70GHz (20 cores)
22:56:52 [App     ] RAM: 62.53GB Physical Memory 8.00GB Virtual Memory
22:56:52 [App     ] OS: Linux 6.17.0-14-generic (x86_64)
22:56:52 [App     ] Disk: 1020.29GB (1.79TB) space
22:56:52 [App     ] SSE & AVX compatible CPU & OS detected
22:56:52 [App     ] Command line: InterfaceCOLMAP -h
22:56:52 [App     ] 
Import/export 3D reconstruction from COLMAP (TXT/BIN format) and to COLMAP (TXT format). 
In order to import a scene, run COLMAP SfM and next undistort the images (only PINHOLE
camera model supported for the moment).
22:56:52 [App     ] Available options:

Generic options:
  -h [ --help ]                         imports SfM or MVS scene stored in 
                                        COLMAP undistoreted format OR exports 
                                        MVS scene to COLMAP format
  -w [ --working-folder ] arg           working directory (default current 
                                        directory)
  -c [ --config-file ] arg (=InterfaceCOLMAP.cfg)
                                        file name containing program options
  --archive-type arg (=4294967295)      project archive type: -1-interface, 
                                        0-text, 1-binary, 2-compressed binary
  --process-priority arg (=-1)          process priority (below normal by 
                                        default)
  --max-threads arg (=0)                maximum number of threads (0 for using 
                                        all available cores)
  -v [ --verbosity ] arg (=2)           verbosity level

Main options:
  -i [ --input-file ] arg               input COLMAP folder containing cameras,
                                        images and points files OR input MVS 
                                        project file
  -p [ --pointcloud-file ] arg          point-cloud with views file name 
                                        (overwrite existing point-cloud)
  -o [ --output-file ] arg              output filename for storing the MVS 
                                        project
  --image-folder arg (=images/)         folder to the undistorted images
  -f [ --normalize ] arg (=0)           normalize intrinsics while exporting to
                                        MVS format
  -e [ --force-points ] arg (=0)        force exporting point-cloud as sparse 
                                        points also even if dense point-cloud 
                                        detected
  --binary arg (=1)                     use binary format for cameras, images 
                                        and points files
  --no-points arg (=0)                  export cameras, images and points files
                                        but not including the sparse 
                                        point-cloud
  --common-intrinsics arg (=0)          force using common intrinsics for all 
                                        camera22:56:52 [App     ] MEMORYINFO: {
22:56:52 [App     ] 	VmPeak:	  252316 kB
22:56:52 [App     ] 	VmSize:	  252280 kB
22:56:52 [App     ] } ENDINFO

```