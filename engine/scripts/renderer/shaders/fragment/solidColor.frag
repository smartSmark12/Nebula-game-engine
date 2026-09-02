#version 330 core

uniform vec4 cols[32]; /* rgba */

flat in uint id; /* from vert shader */

out vec4 f_color;

void main() {
    f_color = cols[id];
}