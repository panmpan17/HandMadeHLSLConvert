# Create a custom HLSL shader convert to GLSL and metal shader

### Type Convertion
                GLSL       Metal
int             int        int
float           float      float
vector2         vec2       float2
vector3         vec3       float3
vector4         vec4       float4
Matrix4x4       mat4       metal::float4x4


### Function
Metal vertex function:
StructPassToFrag 
vertex <StructPassToFrag> <ShaderName>_vertexMain(parameters)
{ ... }

Metal fragment function: (Return the color)
fragment float4 <ShaderName>_fragmentMain(parameters)
{ ... }

GLSL vertex function:
[In .vert file, use 'out' variable to pass to frag]
void main()
{
    gl_Position
}

