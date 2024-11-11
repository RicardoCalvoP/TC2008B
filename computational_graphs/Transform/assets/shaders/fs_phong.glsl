#version 300 es
precision highp float;

in vec4 v_color;
in vec3 v_normal;
in vec3 v_cameraDirection;
in vec3 v_lightDirection;

// Light Uniforms
uniform vec4 u_ambientLight;
uniform vec4 u_diffuseLight;
uniform vec4 u_specularLight;

// Ambient Uniforms
uniform vec4 u_ambientColor;
uniform vec4 u_diffuseColor;
uniform vec4 u_specularColor;
uniform vec4 u_shininess;


out vec4 outColor;

void main() {
    vec4 ambient = u_ambientLight * u_ambientColor;


    outColor = ambient;
}
