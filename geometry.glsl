#version 410 core

layout (triangles) in;
layout (triangle_strip, max_vertices = 3) out;

uniform sampler2D westtex;
uniform sampler2D easttex;

layout (location = 0) in vec2 in_lonlat[];
layout (location = 1) in vec3 in_disp[];
layout (location = 2) in vec3 in_origr[];
layout (location = 0) out vec2 lonlat;
layout (location = 1) out vec3 normal;

uniform mat4 modelrot;
uniform mat4 viewrot;

float getElevation(vec2 geo) {
    float lon = geo.x;
    float lat = 0.5f + 0.5f * geo.y;

    lon -= 2 * floor(0.5f * lon + 0.5f);

    float wwest = 0.5f - 0.5f * sign(lon), weast = 1.0f - wwest;
    return wwest * texture(westtex, vec2(lon + 1.0f, lat)).x +
           weast * texture(easttex, vec2(lon, lat)).x;
}

vec3 computeNormal(vec3 r[3]) {
    vec4 n = vec4(normalize(cross(r[1] - r[0], r[2] - r[0])), 0);
    return (viewrot * modelrot * n).xyz;
}

void main() {
    vec4 newcoord[3];
    vec3 newr[3];
    for (int i = 0; i < 3; i++) {
        newcoord[i] = gl_in[i].gl_Position;
        float h = 0.02 * getElevation(in_lonlat[i]);
        newcoord[i].xyz += h * in_disp[i];
        newr[i] = in_origr[i] * (1 + h);
    }
    vec3 trueNormal = computeNormal(newr);
    for (int i = 0; i < 3; i++) {
	lonlat = in_lonlat[i];
        normal = trueNormal; //normalize(in_disp[i]);//trueNormal;
        gl_Position = newcoord[i];
        EmitVertex();
    }
    EndPrimitive();
}
