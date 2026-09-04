#version 330 core

/* 3f */
in vec3 in_vert;

flat out uint id;

void main() {
    id = uint(gl_VertexID / 3); /* to get the id of the object from vertex id to be used for uniform color access */
    gl_Position = vec4(in_vert, 1.0); /* x, y, d, h */
}