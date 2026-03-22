# 1. RefineMesh -h

```sh
3rd/openMVS/make02/bin$ ./RefineMesh  -h
23:00:48 [App     ] OpenMVS x64 v2.4.0
23:00:48 [App     ] Build date: Feb 22 2026, 20:37:13
23:00:48 [App     ] CPU: Intel(R) Core(TM) i9-10900K CPU @ 3.70GHz (20 cores)
23:00:48 [App     ] RAM: 62.53GB Physical Memory 8.00GB Virtual Memory
23:00:48 [App     ] OS: Linux 6.17.0-14-generic (x86_64)
23:00:48 [App     ] Disk: 1020.29GB (1.79TB) space
23:00:48 [App     ] SSE & AVX compatible CPU & OS detected
23:00:48 [App     ] Command line: RefineMesh -h
23:00:48 [App     ] Available options:

Generic options:
  -h [ --help ]                         produce this help message
  -w [ --working-folder ] arg           working directory (default current 
                                        directory)
  -c [ --config-file ] arg (=RefineMesh.cfg)
                                        file name containing program options
  --export-type arg (=ply)              file type used to export the 3D scene 
                                        (ply or obj)
  --archive-type arg (=4294967295)      project archive type: -1-interface, 
                                        0-text, 1-binary, 2-compressed binary
  --process-priority arg (=-1)          process priority (below normal by 
                                        default)
  --max-threads arg (=0)                maximum number of threads (0 for using 
                                        all available cores)
  -v [ --verbosity ] arg (=2)           verbosity level
  --cuda-device arg (=-2)               CUDA device number to be used for mesh 
                                        refinement (-2 - CPU processing, -1 - 
                                        best GPU, >=0 - device index)

Refine options:
  -i [ --input-file ] arg               input filename containing camera poses 
                                        and image list
  -m [ --mesh-file ] arg                mesh file name to refine (overwrite 
                                        existing mesh)
  -o [ --output-file ] arg              output filename for storing the mesh
  --resolution-level arg (=0)           how many times to scale down the images
                                        before mesh refinement
  --min-resolution arg (=640)           do not scale images lower than this 
                                        resolution
  --max-views arg (=8)                  maximum number of neighbor images used 
                                        to refine the mesh
  --decimate arg (=0)                   decimation factor in range [0..1] to be
                                        applied to the input surface before 
                                        refinement (0 - auto, 1 - disabled)
  --close-holes arg (=30)               try to close small holes in the input 
                                        surface (0 - disabled)
  --ensure-edge-size arg (=1)           ensure edge size and improve vertex 
                                        valence of the input surface (0 - 
                                        disabled, 1 - auto, 2 - force)
  --max-face-area arg (=32)             maximum face area projected in any pair
                                        of images that is not subdivided (0 - 
                                        disabled)
  --scales arg (=2)                     how many iterations to run mesh 
                                        optimization on multi-scale images
  --scale-step arg (=0.5)               image scale factor used at each mesh 
                                        optimization step
  --alternate-pair arg (=0)             refine mesh using an image pair 
                                        alternatively as reference (0 - both, 1
                                        - alternate, 2 - only left, 3 - only 
                                        right)
  --regularity-weight arg (=0.200000003)
                                        scalar regularity weight to balance 
                                        between photo-consistency and 
                                        regularization terms during mesh 
                                        optimization
  --rigidity-elasticity-ratio arg (=0.899999976)
                                        scalar ratio used to compute the 
                                        regularity gradient as a combination of
                                        rigidity and elasticity
  --gradient-step arg (=45.0499992)     gradient step to be used instead (0 - 
                                        auto)
  --planar-vertex-ratio arg (=0)        threshold used to remove vertices on 
                                        planar patches (0 - disabled)
  --reduce-memory arg (=1)              recompute some data in order to reduce 
                                        memory requirement23:00:48 [App     ] MEMORYINFO: {
23:00:48 [App     ] 	VmPeak:	  253296 kB
23:00:48 [App     ] 	VmSize:	  253260 kB
23:00:48 [App     ] } ENDINFO

```