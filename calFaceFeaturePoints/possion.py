import open3d as o3d
# 点云中必须要有法向量
path1 = 'D:/MyFiles/Pictures/0327-2/land57/reg-random08.ply'
path2 = 'D:/MyFiles/Pictures/20220301/left/zhou-random08.ply'
path3 = 'D:/MyFiles/Pictures/20220104/right/di-random08.ply'

face = o3d.io.read_point_cloud(path2)
o3d.visualization.draw_geometries([face])
with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
    mesh , dens = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(face,10)

o3d.visualization.draw_geometries([mesh])
#o3d.io.write_triangle_mesh('D:/MyFiles/Pictures/20220301/left/76-L-rectply-face-down-Mesh.ply',mesh)