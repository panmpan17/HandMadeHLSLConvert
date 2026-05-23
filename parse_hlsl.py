from shader_struct import *


class BracketLevel(Enum):
    NONE = 0
    NORMAL = 1 # Not related to shader struct definitions
    SHADER = 2
    UNIFORM = 3
    VERTEX_INPUT = 4
    VERTEX_OUTPUT = 5
    VERTEX_FUNCTION = 6
    FRAG_FUNCTION = 7


class ParseError(Exception):
    pass


class HLSLParser:
    BRACKET_OPEN = "{"
    BRACKET_CLOSE = "}"
    BRACKET_CLOSE_SEMICOLON = "};"
    SHADER_START = "Shader"
    UNIFORM_START = "struct uniforms"
    VERTEX_INPUT_START = "struct vertexInputs"
    VERTEX_OUTPUT_START = "struct vertexOutputs"
    VERTEX_FUNCTION_START = "vertexOutputs vert("
    FRAG_FUNCTION_START = "float4 frag("

    @classmethod
    def read_file(cls, file_path):
        with open(file_path, "r") as file:
            hlsl_code = file.read()
        return cls(hlsl_code)
    
    @classmethod
    def read_shader_name(cls, line):
        # Example: Shader "MyShader" {
        parts = line.split()
        if len(parts) >= 2:
            return parts[1].strip('"')
        return ""

    def __init__(self, hlsl_code):
        self.hlsl_code = hlsl_code
        self.lines = hlsl_code.splitlines()

        self.shader_struct: ShaderStructure = ShaderStructure()

        self.temp_bracket_level: BracketLevel = BracketLevel.NONE
        self.bracket_levels: list[BracketLevel] = []
    
    @property
    def current_bracket_level(self):
        if self.bracket_levels:
            return self.bracket_levels[-1]
        return BracketLevel.NONE

    def put_bracket_level(self, line, level: BracketLevel):
        if self.temp_bracket_level != BracketLevel.NONE:
            raise ParseError(f"Unexpected bracket level change at line: {line}")
        
        # print(f"Setting temp bracket level to {level.name} at line: {line}")
        if line.endswith(self.BRACKET_OPEN):
            self.bracket_levels.append(level)
        else:
            self.temp_bracket_level = level

    def start_parsing(self):
        for i, line in enumerate(self.lines):
            line = line.strip()

            if len(line) != 0:
                self._parse_line(i, line)

    def _parse_line(self, index, line):
        if line.startswith(self.SHADER_START):
            self.shader_struct.name = self.read_shader_name(line)
            self.put_bracket_level(line, BracketLevel.SHADER)
            return
    
        elif line.startswith(self.UNIFORM_START):
            self.put_bracket_level(line, BracketLevel.UNIFORM)
            return

        elif line.startswith(self.VERTEX_INPUT_START):
            self.put_bracket_level(line, BracketLevel.VERTEX_INPUT)
            return

        elif line.startswith(self.VERTEX_OUTPUT_START):
            self.put_bracket_level(line, BracketLevel.VERTEX_OUTPUT)
            return
        
        elif line.startswith(self.VERTEX_FUNCTION_START):
            self.put_bracket_level(line, BracketLevel.VERTEX_FUNCTION)
            return
    
        elif line.startswith(self.FRAG_FUNCTION_START):
            self.put_bracket_level(line, BracketLevel.FRAG_FUNCTION)
            return
        
        elif line.startswith(self.BRACKET_OPEN):
            if self.temp_bracket_level == BracketLevel.NONE:
                self.bracket_levels.append(BracketLevel.NORMAL)

            else:
                self.bracket_levels.append(self.temp_bracket_level)
                self.temp_bracket_level = BracketLevel.NONE
                # print(f"Entering bracket level: {self.current_bracket_level.name} at line {index + 1}: {line}")
            
            # TODO: If there's more content after bracket, parse it
            return

        elif line.endswith(self.BRACKET_CLOSE) or line.endswith(self.BRACKET_CLOSE_SEMICOLON):
            # TODO: If there's more content before bracket, parse it
            if not self.bracket_levels:
                raise ParseError(f"Unexpected closing bracket at line {index + 1}: {line}")
            self.bracket_levels.pop()
            # print(f"Exiting bracket level, now at: {self.current_bracket_level.name} at line {index + 1}: {line}")
            return
        
        else:
            # for type_name, shader_type in BasicShaderTypeDict.HLSL_NAME_TO_TYPE.items():
            parts = line.split()
            if len(parts) >= 2:
                if parts[0] in BasicShaderTypeDict.HLSL_NAME_TO_TYPE:
                    shader_type = BasicShaderTypeDict.HLSL_NAME_TO_TYPE[parts[0]]
                    # Example: float4 position;
                    field_name = parts[1].rstrip(";")
                    if self.current_bracket_level == BracketLevel.UNIFORM:
                        self.shader_struct.uniform_fields.append(ShaderUniformField(field_name, shader_type))
                    elif self.current_bracket_level == BracketLevel.VERTEX_INPUT:
                        self.shader_struct.vertex_inputs.append(ShaderVertexInput(field_name, shader_type))
                    elif self.current_bracket_level == BracketLevel.VERTEX_OUTPUT:
                        self.shader_struct.vertex_outputs.append(ShaderVertexOutput(field_name, shader_type))
                # break


if __name__ == "__main__":
    parser = HLSLParser.read_file("example/uv/uv.hlsl")
    parser.start_parsing()
    print(parser.shader_struct)
