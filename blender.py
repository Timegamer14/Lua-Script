import bpy,sys
from mathutils import Matrix
from math import radians

def exportMesh(filepath):
    # Only one mesh per scene
    objList = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    
    if len(objList) == 0:
        return
    elif len(objList) > 1:
        return
    # raise exception? dialog box?

    # Process the single mesh object:
    mesh = objList[0]

    # File name is the same as the mesh's name in Blender
    meshFilePath = filepath[0: filepath.rindex('/') + 1] + mesh.name + ".s3d"
    file = open(meshFilePath, 'w', encoding='utf-8')
    
    # Vertex data
    
    file.write('{}\n'.format(len(mesh.data.vertices)))

    for vertex in mesh.data.vertices:
        co = vertex.co
        normal = vertex.normal if mesh.data.polygons[0].use_smooth else mesh.data.polygons[0].normal

        # Assuming one UV layer
        uv_layer = mesh.data.uv_layers[0]
        uv_coord = uv_layer.data[vertex.index].uv

        file.write('{:f} {:f} {:f} {:f} {:f} {:f} {:f} {:f}\n'.format(
            co.x, co.y, co.z,
            normal.x, normal.y, normal.z,
            uv_coord.x, uv_coord.y
        ))
    
    # Indices
    file.write('{}\n'.format(len(mesh.data.polygons) * 3))

    indices = [index for poly in mesh.data.polygons for index in poly.vertices]
    for i, index in enumerate(indices):
        file.write('{} '.format(index))
        if i % 10 == 9:  # Insert line return after every 10 indices
            file.write('\n')

    # Texture name
    
    texture_name = ""
    if len(mesh.material_slots) > 0 and mesh.material_slots[0].material.use_nodes:
        # Check if material has a texture node
        for node in mesh.material_slots[0].material.node_tree.nodes:
            if node.type == 'TEX_IMAGE':
                texture_name = bpy.data.images[node.image.name].name
                break
   
    file.write('\n')
    file.write('{}\n'.format(texture_name))
    
    # Done writing mesh file
    file.close()

# Example usage:
exportMesh("/Cube.s3d")