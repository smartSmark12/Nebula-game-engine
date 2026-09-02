#version 330 core

/* 2f 2f */
in vec2 vert;
in vec2 texcoord;

out vec2 uvs;

void main() {
    uvs = texcoord;
    gl_Position = vec4(vert, 0.0, 1.0); /* x, y, d, h */
}