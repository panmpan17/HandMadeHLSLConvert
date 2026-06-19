import os

from enum import Enum
from pydantic import BaseModel, Field


class BasicShaderType(Enum):
    UNDEFINED = 0

    INT = 1
    FLOAT = 2
    BOOL = 3

    VEC2 = 11
    VEC3 = 12
    VEC4 = 13

    MAT2 = 21
    MAT3 = 22
    MAT4 = 23


class BasicShaderTypeDict:
    HLSL_NAME_TO_TYPE = {
        "int": BasicShaderType.INT,
        "float": BasicShaderType.FLOAT,
        "bool": BasicShaderType.BOOL,
        "float2": BasicShaderType.VEC2,
        "float3": BasicShaderType.VEC3,
        "float4": BasicShaderType.VEC4,
        "float2x2": BasicShaderType.MAT2,
        "float3x3": BasicShaderType.MAT3,
        "float4x4": BasicShaderType.MAT4,
    }
    
    TYPE_TO_METAL_NAME = {
        BasicShaderType.INT: "int",
        BasicShaderType.FLOAT: "float",
        BasicShaderType.BOOL: "bool",
        BasicShaderType.VEC2: "metal::float2",
        BasicShaderType.VEC3: "metal::float3",
        BasicShaderType.VEC4: "metal::float4",
        BasicShaderType.MAT2: "metal::float2x2",
        BasicShaderType.MAT3: "metal::float3x3",
        BasicShaderType.MAT4: "metal::float4x4",
    }
    
    TYPE_TO_GLSL_NAME = {
        BasicShaderType.INT: "int",
        BasicShaderType.FLOAT: "float",
        BasicShaderType.BOOL: "bool",
        BasicShaderType.VEC2: "vec2",
        BasicShaderType.VEC3: "vec3",
        BasicShaderType.VEC4: "vec4",
        BasicShaderType.MAT2: "mat2",
        BasicShaderType.MAT3: "mat3",
        BasicShaderType.MAT4: "mat4",
    }


# @dataclass
class ShaderUniformField(BaseModel):
    name: str
    type: BasicShaderType
    
# @dataclass
class ShaderVertexInput(BaseModel):
    name: str
    type: BasicShaderType


class ShaderVertexOutputMark(Enum):
    NONE = 0
    POSITION = 1
    UV = 2
    COLOR = 3
    NORMAL = 4
    TANGENT = 5
    BITANGENT = 6

SHADER_VERTEX_OUTPUT_MARK_STR_TO_ENUM = {
    "POSITION": ShaderVertexOutputMark.POSITION,
    "UV": ShaderVertexOutputMark.UV,
    "COLOR": ShaderVertexOutputMark.COLOR,
    "NORMAL": ShaderVertexOutputMark.NORMAL,
    "TANGENT": ShaderVertexOutputMark.TANGENT,
    "BITANGENT": ShaderVertexOutputMark.BITANGENT,
}

# @dataclass
class ShaderVertexOutput(BaseModel):
    name: str
    type: BasicShaderType
    mark: ShaderVertexOutputMark

# @dataclass
class ShaderStructure(BaseModel):
    name: str = ""
    uniform_fields: list[ShaderUniformField] = Field(default_factory=list) 
    vertex_inputs: list[ShaderVertexInput] = Field(default_factory=list) 
    vertex_outputs: list[ShaderVertexOutput] = Field(default_factory=list) 

    @classmethod
    def from_file(cls, file_path):
        # json_data = '{"name": "Alice", "status": "active", "address": {"city": "Taipei", "zip_code": "114"}}'
        if not os.path.isfile(file_path):
            raise Exception(f"No such file '{file_path}'")
        
        with open(file_path) as f:
            content = f.read()
        
        data = cls.model_validate_json(content)
        return data
