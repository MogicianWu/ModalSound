This directory is used for cleaning up meshes before using them in isostuff program. In order for isostuffer to work properly, the following conditions must be met:

a) The mesh is watertight
b) The mesh has only one connected component
c) The mesh is consistently originated, all faces order point outward
d) The triangles don't have too small areas
e) The mesh doesn't have duplicate vertices
f) The mesh is a triangle mesh
h) The mesh should only contain face and vertices information

The files in IsoStuffer/tools folder handles case b), c), d), e) f), and user can implement a) and h). User need to install gptoolbox from github repo https://github.com/alecjacobson/gptoolbox, and meshlab on linux.

User can first call convert_mesh.py and specify input/output mesh directories. This script will call a meshlab script on each mesh to first convert all meshes into a triangle mesh and then reorient them consistently. 

There are two useful matlab scripts in /mesh_cleanup folder. run_meshes.m will call meshclean.m script which will remove duplicate vertices, faces with too small areas, and unreferenced vertices.

During our experiment we used meshes from Thingi10k database (https://ten-thousand-models.appspot.com/), which comes with an excel file noting which meshes have more than one connected component. This method is implemented in get_info.py with option 2. If user are using other meshes they need to make sure this is true in some other ways.

gen_tet.py will call IsoStuffer on a directory of meshes. Should future errors be thrown in IsoStuffer program, one can use this file and get_info.py to see which type of errors it produced.