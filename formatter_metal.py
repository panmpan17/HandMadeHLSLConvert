import os

from typing import Optional
from shader_struct import ShaderStructure, BasicShaderTypeDict, ShaderVertexOutputMark



class MetalFormatter:
    def __init__(self):
        self.target_struct: Optional[ShaderStructure] = None
        self.file_content = ""
    
    
    # Formatter Virtual method
    def start_format(self, struct: ShaderStructure,
                     output_folder: str = "output",
                     filename_prefix="", filename_suffix=""):
        self.target_struct = struct
        
        self._add_header()
        self._add_uniform_struct()
        self._add_vertex_in_struct()
        self._add_vertex_out_struct()
        
        file_name = f"{filename_prefix}{struct.name}{filename_suffix}.metal"
        output_file_path = os.path.join(output_folder, file_name)
        with open(output_file_path, "w") as f:
            f.write(self.file_content)
    

    # Custom formatter method
    def _add_header(self):
        self.file_content += "#include <metal_stdlib>\n\n"
    
    def _add_uniform_struct(self):
        self.file_content += f"struct {self.target_struct.name}_Uniforms\n{{\n"

        for uniform in self.target_struct.uniform_fields:
            self.file_content += "\t"
            self.file_content += BasicShaderTypeDict.TYPE_TO_METAL_NAME[uniform.type]
            self.file_content += " "
            self.file_content += uniform.name
            self.file_content += ";\n"

        self.file_content += "};\n\n"

    def _add_vertex_in_struct(self):
        self.file_content += f"struct {self.target_struct.name}_VertexIn\n{{\n"

        for i, vertex in enumerate(self.target_struct.vertex_inputs):
            self.file_content += "\t"
            self.file_content += BasicShaderTypeDict.TYPE_TO_METAL_NAME[vertex.type]
            self.file_content += " "
            self.file_content += vertex.name
            self.file_content += f" [[attribute({i})]];\n"

        self.file_content += "};\n\n"

    def _add_vertex_out_struct(self):
        self.file_content += f"struct {self.target_struct.name}_VertexOut\n{{\n"

        for vertex in self.target_struct.vertex_outputs:
            self.file_content += "\t"
            self.file_content += BasicShaderTypeDict.TYPE_TO_METAL_NAME[vertex.type]
            self.file_content += " "
            self.file_content += vertex.name
            
            if vertex.mark == ShaderVertexOutputMark.POSITION:
                self.file_content += " [[position]]"
            
            self.file_content += ";\n"


        self.file_content += "};\n\n"


if __name__ == "__main__":
    formatter = MetalFormatter()
    shader_struct = ShaderStructure.from_file("output/uv_struct.txt")
    formatter.start_format(shader_struct, output_folder="output")
