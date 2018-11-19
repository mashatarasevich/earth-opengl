#version 410 core

layout (location = 0) in vec2 lonlat;

uniform sampler2D surfwest;
uniform sampler2D surfeast;

out vec4 color;

vec4 getColor(vec2 geo) {
    float lon = geo.x;
    float lat = 0.5f + 0.5f * geo.y;

    float wwest = 0.5f - 0.5f * sign(lon), weast = 1.0f - wwest;
    return wwest * texture(surfwest, vec2(lon + 1.0f, lat)) +
           weast * texture(surfeast, vec2(lon, lat));
}

void main() {
    color = getColor(lonlat);
}
