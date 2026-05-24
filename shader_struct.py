from enum import Enum
from dataclasses import dataclass, field


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


@dataclass
class ShaderUniformField:
    name: str
    type: BasicShaderType
    
@dataclass
class ShaderVertexInput:
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

@dataclass
class ShaderVertexOutput:
    name: str
    type: BasicShaderType
    mark: ShaderVertexOutputMark

@dataclass
class ShaderStructure:
    name: str = ""
    uniform_fields: list[ShaderUniformField] = field(default_factory=list) 
    vertex_inputs: list[ShaderVertexInput] = field(default_factory=list) 
    vertex_outputs: list[ShaderVertexOutput] = field(default_factory=list) 
