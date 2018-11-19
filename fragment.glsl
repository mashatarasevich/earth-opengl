#version 410 core

layout (location = 0) in vec2 lonlat;
layout (location = 1) in vec3 normal;

uniform sampler2D surfwest;
uniform sampler2D surfeast;
uniform vec4 trans;
uniform int grid;
uniform int normals;

out vec4 color;

vec4 getColor(vec2 geo) {
    float lon = geo.x;
    float lat = 0.5f + 0.5f * geo.y;

    lon -= 2 * floor(0.5f * lon + 0.5f);

    if (lon < 0)
    	return texture(surfwest, vec2(lon + 1.0f, lat));
    else
        return texture(surfeast, vec2(lon, lat));
}

void main() {
    vec4 surf = getColor(lonlat);
    const float pi = 3.14159265358979323f;
    if (grid == 1) {
        float c1 = sin(12 * pi * lonlat.x) * cos(lonlat.y * 0.5 * pi);
        float c2 = sin(6 * pi * lonlat.y);
        float d = trans.z - 1.0f;
        c1 /= d;
        c2 /= d;
        float c = min(c1*c1, c2*c2);
        float w = exp(-1600 * c);

        vec4 gridColor = vec4(1.0f, 0.6f, 0.f, 0);
        
        surf = (1-w)*surf + w * gridColor;
    }
    if (normals == 1) {
        color = vec4(0.5 + 0.5 * normal, 1);
    } else {
        float prod = dot(normal, vec3(0.6, 0, 0.8));
        color = surf * (0.3 + 0.7 * max(prod, 0));
    }
}
