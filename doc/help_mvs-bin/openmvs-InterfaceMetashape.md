# 1.InterfaceMetashape -h
```sh
3rd/openMVS/make02/bin$ ./InterfaceMetashape -h
22:58:45 [App     ] OpenMVS x64 v2.4.0
22:58:45 [App     ] Build date: Feb 22 2026, 20:37:13
22:58:45 [App     ] CPU: Intel(R) Core(TM) i9-10900K CPU @ 3.70GHz (20 cores)
22:58:45 [App     ] RAM: 62.53GB Physical Memory 8.00GB Virtual Memory
22:58:45 [App     ] OS: Linux 6.17.0-14-generic (x86_64)
22:58:45 [App     ] Disk: 1020.29GB (1.79TB) space
22:58:45 [App     ] SSE & AVX compatible CPU & OS detected
22:58:45 [App     ] Command line: InterfaceMetashape -h
22:58:45 [App     ] Available options:

Generic options:
  -h [ --help ]                         imports SfM scene stored either in 
                                        Metashape Agisoft/BlocksExchange or 
                                        ContextCapture BlocksExchange XML 
                                        format
  -w [ --working-folder ] arg           working directory (default current 
                                        directory)
  -c [ --config-file ] arg (=InterfaceMetashape.cfg)
                                        file name containing program options
  --archive-type arg (=4294967295)      project archive type: -1-interface, 
                                        0-text, 1-binary, 2-compressed binary
  --process-priority arg (=-1)          process priority (below normal by 
                                        default)
  --max-threads arg (=0)                maximum number of threads (0 for using 
                                        all available cores)
  -v [ --verbosity ] arg (=2)           verbosity level

Main options:
  -i [ --input-file ] arg               input filename containing camera poses 
                                        and image list
  -p [ --points-file ] arg              input filename containing the 3D points
  -o [ --output-file ] arg              output filename for storing the scene
  --output-image-folder arg (=undistorted_images)
                                        output folder to store undistorted 
                                        images
22:58:45 [App     ] MEMORYINFO: {
22:58:45 [App     ] 	VmPeak:	  256260 kB
22:58:45 [App     ] 	VmSize:	  256224 kB
22:58:45 [App     ] } ENDINFO
```