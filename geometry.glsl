#version 410 core

layout (triangles) in;
layout (triangle_strip, max_vertices = 3) out;

uniform sampler2D westtex;
uniform sampler2D easttex;

layout (location = 0) in vec2 in_lonlat[];
layout (location = 1) in vec3 in_normal[];
layout (location = 0) out vec2 lonlat;
layout (location = 1) out vec3 normal;

float getElevation(vec2 geo) {
    float lon = geo.x;
    float lat = 0.5f + 0.5f * geo.y;

    float wwest = 0.5f - 0.5f * sign(lon), weast = 1.0f - wwest;
    return wwest * texture(westtex, vec2(lon + 1.0f, lat)).x +
           weast * texture(easttex, vec2(lon, lat)).x;
}

void main() {
    for (int i = 0; i < 3; i++) {
	lonlat = in_lonlat[i];
        normal = in_normal[i];
        gl_Position = gl_in[i].gl_Position;
        gl_Position.xyz += 0.02 * getElevation(lonlat) * normal;
        EmitVertex();
    }
    EndPrimitive();
}
