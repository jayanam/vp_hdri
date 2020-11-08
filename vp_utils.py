import bpy, os

def get_preview_image(space,add=True):
    """
    Get the active studio light and open the image
    """
    prev_type = space.shading.type
    space.shading.type = "RENDERED"
    light = space.shading.selected_studio_light
    space.shading.type = prev_type
    if os.path.exists(light.path):
        if add: bpy.ops.image.open(filepath=light.path)
        return bpy.data.images[light.name]
    return None
    

def set_active_output(nodes,output=None):
    """
    Sets the active output node in the world node tree
    """
    for node in nodes:
        if node.type == 'OUTPUT_WORLD':
            if output: node.is_active_output = False
            else: node.is_active_output = True
    if output: output.is_active_output = True

def add_nodes_to_world(space):
    """
    Add the environment nodes to the world tree
    """
    tree = bpy.context.scene.world.node_tree
    nodes = tree.nodes
    links = tree.links
    image = get_preview_image(space)

    if image:
        output = nodes.new("ShaderNodeOutputWorld")
        background = nodes.new("ShaderNodeBackground")
        mix = nodes.new("ShaderNodeMixRGB")
        math = nodes.new("ShaderNodeMath")
        light = nodes.new("ShaderNodeLightPath")
        environment = nodes.new("ShaderNodeTexEnvironment")
        mapping = nodes.new("ShaderNodeMapping")
        coords = nodes.new("ShaderNodeTexCoord")

        links.new(coords.outputs[0],mapping.inputs[0])
        links.new(mapping.outputs[0],environment.inputs[0])
        links.new(light.outputs[0],math.inputs[0])
        links.new(math.outputs[0],mix.inputs[0])
        links.new(environment.outputs[0],mix.inputs[1])
        links.new(mix.outputs[0],background.inputs[0])
        links.new(background.outputs[0],output.inputs[0])

        output.label = "out_prev_for_hdr"
        background.inputs[1].default_value = space.shading.studiolight_intensity
        math.inputs[1].default_value = 1 - space.shading.studiolight_background_alpha
        math.operation = "MULTIPLY"
        mix.inputs[2].default_value = (0.050876,0.050876,0.050876,1)
        environment.image = image
        mapping.inputs[2].default_value[2] = space.shading.studiolight_rotate_z
        set_active_output(nodes,output)
    else:
        print("Couldn't find preview image")

def remove_nodes_from_world():
    """
    Remove the environment nodes from the world tree
    """
    nodes = bpy.context.scene.world.node_tree.nodes

    output = None
    for node in nodes:
        if node.label == "out_prev_for_hdr":
            output = node

    if output:
        background = output.inputs[0].links[0].from_node
        mix = background.inputs[0].links[0].from_node
        math = mix.inputs[0].links[0].from_node
        light = math.inputs[0].links[0].from_node
        environment = mix.inputs[1].links[0].from_node
        mapping = environment.inputs[0].links[0].from_node
        coords = mapping.inputs[0].links[0].from_node
        
        bpy.data.images.remove(environment.image)
        nodes.remove(output)
        nodes.remove(background)
        nodes.remove(mix)
        nodes.remove(math)
        nodes.remove(light)
        nodes.remove(environment)
        nodes.remove(mapping)
        nodes.remove(coords)
        set_active_output(nodes)