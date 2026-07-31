# version 330 core

in vec3 vert;
in vec2 texcoord;

out vec2 uvs;

void main () {
    uvs = texcoord;
    gl_Position = vec4(vert, 1.0);
}