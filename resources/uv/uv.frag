#version 330

in vec2 frag_uv;

out vec4 fragment;

void main()
{
    fragment = vec4(frag_uv, 0.0, 1.0);
}
