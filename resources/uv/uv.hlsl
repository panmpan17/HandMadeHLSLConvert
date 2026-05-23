Shader "uv"
{
    struct uniforms
    {
        float4x4 MVPMatrix;
    };

    struct vertexInputs
    {
        float3 position;
        float2 uv;
    };

    struct vertexOutputs
    {
        float4 position : POSITION;
        float2 uv;
    };

    vertexOutputs vert(uniforms u, vertexInputs v)
    {
        vertexOutputs o
        {
            position = mul(u.MVPMatrix, float4(v.position, 0.0, 1.0)),
            uv = v.uv
        };

        return o;
    }


    float4 frag(vertexOutputs _in)
    {
        return float4(_in.uv, 0.0, 1.0);
    }
}