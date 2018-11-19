#version 410 core

layout (vertices = 3) out;

layout (location = 0) in vec2 in_lonlat[];
layout (location = 0) out vec2 lonlat[];
layout (location = 1) in vec3 in_disp[];
layout (location = 1) out vec3 disp[];
layout (location = 2) in vec3 in_origr[];
layout (location = 2) out vec3 origr[];

uniform int adaptive_tess;

float distcam(vec3 pos) {
    return length(pos);
}

float fix_lon(bool fix_needed, float x) {
    if (fix_needed && x < -0.5f) {
        return x + 2.0f;
    }
    return x;
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

    if (adaptive_tess == 1) {
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
    } else {
        for (int i = 0; i < 3; i++)
            gl_TessLevelOuter[i] = 1;
    }

    gl_TessLevelInner[0] = max(gl_TessLevelOuter[0], max(gl_TessLevelOuter[1], gl_TessLevelOuter[2]));

    gl_out[gl_InvocationID].gl_Position = gl_in[gl_InvocationID].gl_Position;
    vec2 geo = in_lonlat[gl_InvocationID];
    geo.x = fix_lon(fix_needed, geo.x);
    if (abs(geo.y) > 0.9999) { // fix longtitude for poles
        int j1 = (gl_InvocationID + 1) % 3;
        int j2 = (gl_InvocationID + 2) % 3;
        geo.x = 0.5f * (fix_lon(fix_needed, in_lonlat[j1].x) + 
                        fix_lon(fix_needed, in_lonlat[j2].x));
    }
    lonlat[gl_InvocationID] = geo;
    disp[gl_InvocationID] = in_disp[gl_InvocationID];
    origr[gl_InvocationID] = in_origr[gl_InvocationID];
}
