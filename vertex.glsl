#version 410 core

layout (location = 0) in vec3 pos;
layout (location = 1) in vec2 inlonlat;

layout (location = 0) out vec2 lonlat;
layout (location = 1) out vec3 normal;

uniform mat4 proj;
uniform mat4 modelrot;
uniform mat4 viewrot;
uniform vec4 trans;

void main() {
    vec4 point = vec4(pos, 1.0f);
    gl_Position = proj * viewrot * (modelrot * point - trans);
    lonlat = inlonlat;
    normal = (proj * viewrot * modelrot * vec4(pos, 0)).xyz;
}
