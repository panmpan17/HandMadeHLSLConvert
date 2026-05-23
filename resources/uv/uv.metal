#include <metal_stdlib>


struct image_Uniforms
{
    metal::float4x4 MVPMatrix;
};

struct image_VertexIn
{
    float3 position [[attribute(0)]];
    float2 texCoord [[attribute(1)]];
};

struct image_VertexOut
{
    metal::float4 position [[position]];
    metal::float2 texCoord;
};


vertex image_VertexOut image_vertexMain(image_VertexIn in [[stage_in]],
                                        constant image_Uniforms& uniforms [[buffer(2)]])
{
    image_VertexOut out;
    out.position = uniforms.MVPMatrix * metal::float4(in.position, 1.0);
    out.texCoord = in.texCoord;
    return out;
}

fragment metal::float4 image_fragmentMain(image_VertexOut in [[stage_in]])
{
    return metal::float4(in.texCoord, 0.0, 1.0);
}

//  xcrun -sdk macosx metal -o assets/metal_shaders/colored_vertices.ir  -c assets/metal_shaders/colored_vertices.metal
//  xcrun -sdk macosx metal -o assets/metal_shaders.metallib assets/metal_shaders/colored_vertices.ir