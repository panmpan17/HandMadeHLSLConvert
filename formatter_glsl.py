import os

from typing import Optional
from shader_struct import ShaderStructure, BasicShaderTypeDict, ShaderVertexOutputMark



class GLSLFormatter:
    VERSION_330 = 330

    def __init__(self):
        self.target_struct: Optional[ShaderStructure] = None
        self.frag_content = ""
        self.vert_content = ""
        self.version = self.VERSION_330
    

    # Formatter Virtual method
    def start_format(self, struct: ShaderStructure,
                     output_folder: str = "output",
                     filename_prefix="", filename_suffix=""):
        self.target_struct = struct
        
        self._add_version_declare()
        self._add_uniform_struct()
        self._add_vertex_in_struct()
        self._add_vertex_out_struct()
        self._add_frag_main()
        self._add_vertex_main()
        
        frag_file_name = f"{filename_prefix}{struct.name}{filename_suffix}.frag"
        frag_file_path = os.path.join(output_folder, frag_file_name)
        with open(frag_file_path, "w") as f:
            f.write(self.frag_content)

        vert_file_name = f"{filename_prefix}{struct.name}{filename_suffix}.vert"
        vert_file_path = os.path.join(output_folder, vert_file_name)
        with open(vert_file_path, "w") as f:
            f.write(self.vert_content)
    

    # Custom formatter method
    def _add_version_declare(self):
        self.frag_content += f"#version {self.version}\n\n"
        self.vert_content += f"#version {self.version}\n\n"
    
    def _add_uniform_struct(self):
        def content_add_uniform(content):
            for uniform in self.target_struct.uniform_fields:
                content += "uniform "
                content += BasicShaderTypeDict.TYPE_TO_GLSL_NAME[uniform.type]
                content += " u_"
                content += uniform.name
                content += ";\n"
            content += "\n"
            return content
    
        self.frag_content = content_add_uniform(self.frag_content)
        self.vert_content = content_add_uniform(self.vert_content)
    
    def _add_vertex_in_struct(self):
        for i, vertex in enumerate(self.target_struct.vertex_inputs):
            self.vert_content += f"layout (location = {i}) in "
            self.vert_content += BasicShaderTypeDict.TYPE_TO_GLSL_NAME[vertex.type]
            self.vert_content += " in_"
            self.vert_content += vertex.name
            self.vert_content += f";\n"
        self.vert_content += "\n"
    
    def _add_vertex_out_struct(self):
        for vertex in self.target_struct.vertex_outputs:
            self.vert_content += "out "
            self.vert_content += BasicShaderTypeDict.TYPE_TO_GLSL_NAME[vertex.type]
            self.vert_content += " frag_"
            self.vert_content += vertex.name
            self.vert_content += ";\n"

            if vertex.mark != ShaderVertexOutputMark.POSITION:
                self.frag_content += "in "
                self.frag_content += BasicShaderTypeDict.TYPE_TO_GLSL_NAME[vertex.type]
                self.frag_content += " frag_"
                self.frag_content += vertex.name
                self.frag_content += ";\n"

        self.vert_content += "\n"
        self.frag_content += "\n"
    
    def _add_frag_main(self):
        self.frag_content += "void main()\n{\n"

        self.frag_content += "}\n"

    def _add_vertex_main(self):
        self.vert_content += "out vec4 fragment;\n\nvoid main()\n{\n"

        self.vert_content += "}\n"


if __name__ == "__main__":
    formatter = GLSLFormatter()
    shader_struct = ShaderStructure.from_file("output/uv_struct.txt")
    formatter.start_format(shader_struct, output_folder="output")
