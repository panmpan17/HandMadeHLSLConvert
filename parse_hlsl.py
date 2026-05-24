import re

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
    
    VARIABLE_DECLARATION_REGEX = r"[a-zA-Z_][a-zA-Z_0-9]+[\s]+[a-zA-Z_][a-zA-Z_0-9]+[\s*]?;"
    VARIABLE_DECLARATION_WITH_MARK_REGEX = r"[a-zA-Z_][a-zA-Z_0-9]+[\s]+[a-zA-Z_][a-zA-Z_0-9]+[\s]*?\:[\s]*[a-zA-Z_0-9]+[\s]*;"

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
    
    def reset(self):
        self.shader_struct = ShaderStructure()
        self.temp_bracket_level = BracketLevel.NONE
        self.bracket_levels.clear()
    
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
        if self._parse_brcket_strucutre_by_line(index, line):
            return
    
        variable_decl_matches = re.findall(self.VARIABLE_DECLARATION_REGEX, line)
        if variable_decl_matches:
            for decl_match in variable_decl_matches:
                parts = decl_match.split()
                if len(parts) < 2:
                    raise ParseError(f"Invalid variable declaration at line {index + 1}: {decl_match}")

                if parts[0] not in BasicShaderTypeDict.HLSL_NAME_TO_TYPE:
                    raise ParseError(f"Unknown type '{parts[0]}' at line {index + 1}: {line}")
                
                shader_type = BasicShaderTypeDict.HLSL_NAME_TO_TYPE[parts[0]]
                field_name = parts[1].rstrip(";")

                if self.current_bracket_level == BracketLevel.UNIFORM:
                    self.shader_struct.uniform_fields.append(ShaderUniformField(field_name, shader_type))
                elif self.current_bracket_level == BracketLevel.VERTEX_INPUT:
                    self.shader_struct.vertex_inputs.append(ShaderVertexInput(field_name, shader_type))
                elif self.current_bracket_level == BracketLevel.VERTEX_OUTPUT:
                    self.shader_struct.vertex_outputs.append(ShaderVertexOutput(field_name, shader_type, ShaderVertexOutputMark.NONE))
                
                # TODO: Normal variable declaration?
        
        variable_decl_with_mark_matches = re.findall(self.VARIABLE_DECLARATION_WITH_MARK_REGEX, line)
        if variable_decl_with_mark_matches:
            for decl_match in variable_decl_with_mark_matches:
                column_index = decl_match.find(":")
                if column_index == -1:
                    raise ParseError(f"Invalid variable declaration with mark at line {index + 1}: {decl_match}")
            
                field_parts = decl_match[:column_index].split()
                if len(field_parts) < 2:
                    raise ParseError(f"Invalid variable declaration with mark at line {index + 1}: {decl_match}")
                if field_parts[0] not in BasicShaderTypeDict.HLSL_NAME_TO_TYPE:
                    raise ParseError(f"Unknown type '{field_parts[0]}' at line {index + 1}: {line}")
                
                shader_type = BasicShaderTypeDict.HLSL_NAME_TO_TYPE[field_parts[0]]
                field_name = field_parts[1]
                
                mark_name = decl_match[column_index + 1:].strip().rstrip(";")
                if mark_name.upper() not in SHADER_VERTEX_OUTPUT_MARK_STR_TO_ENUM:
                    raise ParseError(f"Unknown mark '{mark_name}' at line {index + 1}: {line}")
                mark = SHADER_VERTEX_OUTPUT_MARK_STR_TO_ENUM[mark_name.upper()]
                print(shader_type, field_name, mark)
                
                if self.current_bracket_level == BracketLevel.VERTEX_OUTPUT:
                    self.shader_struct.vertex_outputs.append(ShaderVertexOutput(field_name, shader_type, mark))
                else:
                    raise ParseError(f"Variable declaration with mark is only allowed in vertex output struct at line {index + 1}: {line}")

    
    def _parse_brcket_strucutre_by_line(self, index, line):
        if line.startswith(self.SHADER_START):
            self.shader_struct.name = self.read_shader_name(line)
            self.put_bracket_level(line, BracketLevel.SHADER)
            return True
    
        elif line.startswith(self.UNIFORM_START):
            self.put_bracket_level(line, BracketLevel.UNIFORM)
            return True

        elif line.startswith(self.VERTEX_INPUT_START):
            self.put_bracket_level(line, BracketLevel.VERTEX_INPUT)
            return True

        elif line.startswith(self.VERTEX_OUTPUT_START):
            self.put_bracket_level(line, BracketLevel.VERTEX_OUTPUT)
            return True
        
        elif line.startswith(self.VERTEX_FUNCTION_START):
            self.put_bracket_level(line, BracketLevel.VERTEX_FUNCTION)
            return True
    
        elif line.startswith(self.FRAG_FUNCTION_START):
            self.put_bracket_level(line, BracketLevel.FRAG_FUNCTION)
            return True
        
        elif line.endswith(self.BRACKET_OPEN):
            if self.temp_bracket_level == BracketLevel.NONE:
                self.bracket_levels.append(BracketLevel.NORMAL)

            else:
                self.bracket_levels.append(self.temp_bracket_level)
                self.temp_bracket_level = BracketLevel.NONE
                # print(f"Entering bracket level: {self.current_bracket_level.name} at line {index + 1}: {line}")
            
            # TODO: If there's more content after bracket, parse it
            return True

        elif line.endswith(self.BRACKET_CLOSE) or line.endswith(self.BRACKET_CLOSE_SEMICOLON):
            # TODO: If there's more content before bracket, parse it
            if not self.bracket_levels:
                raise ParseError(f"Unexpected closing bracket at line {index + 1}: {line}")
            self.bracket_levels.pop()
            # print(f"Exiting bracket level, now at: {self.current_bracket_level.name} at line {index + 1}: {line}")
            return True
        
        return False


if __name__ == "__main__":
    parser = HLSLParser.read_file("resources/uv/uv.hlsl")
    parser.start_parsing()
    print(parser.shader_struct)
