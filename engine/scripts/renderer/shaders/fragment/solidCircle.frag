#version 330 core

uniform vec4 cols[64]; /* rgba */
uniform vec2 centers[64]; /* circle center (px, px) */
uniform float radii[64]; /* circle radius (px) */
uniform float widths[64]; /* circle edge width (px) */

flat in uint id; /* from vert shader */

out vec4 f_color;

void main() {
    vec4 color = cols[id];
    vec2 center = centers[id];
    float radius = radii[id];
    float width = widths[id];

    if (width == 0.0) { /* this is kind of a stupid way to do it, but it's for pygame compatibility */
        width = radius;
    }

    float dist = distance(center, gl_FragCoord.xy);

    f_color = vec4( dist < radius && dist > (radius - width) ) * color;
}