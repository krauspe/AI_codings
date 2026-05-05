import bpy
import math

# Clear scene
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

clear_scene()

# Set dark universe background
bpy.context.scene.world.use_nodes = True
bg = bpy.context.scene.world.node_tree.nodes['Background']
bg.inputs[0].default_value = (0.01, 0.01, 0.05, 1)

# Wormhole lattice parameters (catenoid shape)
segments_length = 64
segments_circle = 32
length = 8.0
min_radius = 1.0

verts = []
edges = []

for i in range(segments_length):
    t = (i / (segments_length - 1)) * 2 - 1  # t in [-1, 1]
    radius = min_radius * math.cosh(t)
    z = length * t * 0.5
    for j in range(segments_circle):
        # Create a sheet by not making a full circle, leaving a gap.
        angle = (2 * math.pi * 0.9) * j / (segments_circle - 1)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        verts.append((x, y, z))

for i in range(segments_length):
    for j in range(segments_circle):
        idx = i * segments_circle + j
        # Edges along the circle's arc
        if j < segments_circle - 1:
            edges.append((idx, idx + 1))
        # Edges along the length of the wormhole
        if i < segments_length - 1:
            edges.append((idx, idx + segments_circle))

# Add faces to create a single sheet surface from upper to lower hole
faces = []
for i in range(segments_length - 1):
    for j in range(segments_circle - 1):
        idx0 = i * segments_circle + j
        idx1 = i * segments_circle + j + 1
        idx2 = (i + 1) * segments_circle + j + 1
        idx3 = (i + 1) * segments_circle + j
        faces.append([idx0, idx1, idx2, idx3])

mesh = bpy.data.meshes.new("WormholeLattice")
mesh.from_pydata(verts, edges, faces)
obj = bpy.data.objects.new("WormholeLattice", mesh)
bpy.context.collection.objects.link(obj)

# Material with blue (top) and yellow (bottom) gradient
mat = bpy.data.materials.new(name="WormholeGradient")
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links

nodes.clear()
output = nodes.new(type='ShaderNodeOutputMaterial')
diffuse = nodes.new(type='ShaderNodeBsdfDiffuse')
separate_xyz = nodes.new(type='ShaderNodeSeparateXYZ')
coord = nodes.new(type='ShaderNodeGeometry')
color_ramp = nodes.new(type='ShaderNodeValToRGB')

color_ramp.color_ramp.elements[0].color = (0.1, 0.2, 0.8, 1)  # Blue (top)
color_ramp.color_ramp.elements[1].color = (0.9, 0.8, 0.1, 1)  # Yellow (bottom)

# Connect nodes for vertical gradient
links.new(coord.outputs['Position'], separate_xyz.inputs['Vector'])
links.new(separate_xyz.outputs['Z'], color_ramp.inputs['Fac'])
links.new(color_ramp.outputs['Color'], diffuse.inputs['Color'])
links.new(diffuse.outputs['BSDF'], output.inputs['Surface'])

obj.data.materials.append(mat)

# Smooth shading
bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.context.view_layer.objects.active = obj
bpy.ops.object.shade_smooth()
