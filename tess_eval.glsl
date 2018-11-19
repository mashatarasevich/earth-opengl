#version 410 core

layout (triangles, equal_spacing, ccw) in;

layout (location = 0) in vec2 in_lonlat[];
layout (location = 0) out vec2 lonlat;
layout (location = 1) in vec3 in_disp[];
layout (location = 1) out vec3 disp;
layout (location = 2) in vec3 in_origr[];
layout (location = 2) out vec3 origr;

void main()
{ 
    gl_Position =
        gl_in[0].gl_Position * gl_TessCoord.x + 
        gl_in[1].gl_Position * gl_TessCoord.y + 
        gl_in[2].gl_Position * gl_TessCoord.z;
    lonlat = 
        in_lonlat[0] * gl_TessCoord.x + 
        in_lonlat[1] * gl_TessCoord.y + 
        in_lonlat[2] * gl_TessCoord.z;
    disp = 
        in_disp[0] * gl_TessCoord.x + 
        in_disp[1] * gl_TessCoord.y + 
        in_disp[2] * gl_TessCoord.z;
    origr = 
        in_origr[0] * gl_TessCoord.x + 
        in_origr[1] * gl_TessCoord.y + 
        in_origr[2] * gl_TessCoord.z;
}
