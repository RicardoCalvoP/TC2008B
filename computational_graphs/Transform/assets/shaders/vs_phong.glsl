#version 300 es
in vec4 a_position;
in vec4 a_normal;
in vec4 a_color;

// Global Uniforms
uniform vec4 u_viewWorldPosition;
uniform vec4 u_lightWorldPosition;

// Model Uniforms
uniform mat4 u_world;
uniform mat4 u_worldInverseTransform;
uniform mat4 u_worldViewProjection;

out vec3 v_normal;
out vec3 v_cameraDirection;
out vec3 v_lightDirection;
out vec4 v_color;

void main() {
    gl_Position = u_worldViewProjection * a_position;
    v_normal = normalize(u_world * a_normal).xyz;
    v_lightDirection = normalize(u_lightWorldPosition - gl_Position).xyz;
    v_cameraDirection = normalize(u_viewWorldPosition - gl_Position).xyz;
    v_color = a_color;
}
