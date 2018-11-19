#version 410 core

layout (vertices = 3) out;

layout (location = 0) in vec2 in_lonlat[];
layout (location = 0) out vec2 lonlat[];
layout (location = 1) in vec3 in_normal[];
layout (location = 1) out vec3 normal[];

float distcam(vec3 pos) {
    return length(pos);
}

void main() {
    bool some_are_on_the_left = false;
    bool some_are_on_the_right = false;
    for (int i = 0; i < 3; i++) {
        float lon = in_lonlat[i].x;
        if (lon < -0.5)
            some_are_on_the_left = true;
        if (lon > 0.5)
            some_are_on_the_right = true;
    }

    bool fix_needed = some_are_on_the_left && some_are_on_the_right;

    for (int i = 0; i < 3; i++) {
        vec3 midpoint = 0.5 * (
            gl_in[(i + 1) % 3].gl_Position.xyz +
            gl_in[(i + 2) % 3].gl_Position.xyz
        );
        float dist = distcam(midpoint);
        if (dist < 0.3)
            gl_TessLevelOuter[i] = 8;
        else if (dist < 0.6)
            gl_TessLevelOuter[i] = 4;
        else if (dist < 1)
            gl_TessLevelOuter[i] = 2;
        else
            gl_TessLevelOuter[i] = 1;
    }

    gl_TessLevelInner[0] = max(gl_TessLevelOuter[0], max(gl_TessLevelOuter[1], gl_TessLevelOuter[2]));

    gl_out[gl_InvocationID].gl_Position = gl_in[gl_InvocationID].gl_Position;
    lonlat[gl_InvocationID] = in_lonlat[gl_InvocationID];
    if (fix_needed && (lonlat[gl_InvocationID].x < -0.5)) {
        lonlat[gl_InvocationID].x += 2;
    }
    normal[gl_InvocationID] = in_normal[gl_InvocationID];
}
