/*
 * Script to draw a complex shape in 2D
 *
 * Ricardo Alfredo Calvo Perez
 */


'use strict';

import * as twgl from 'twgl-base.js'
import { shapeF } from '../00_common/shapes.js'
import { m3 } from '../libs/libs2D.js';
import GUI from 'lil-gui';

// Define the shader code, using GLSL 3.00

const vsGLSL = `#version 300 es
in vec2 a_position;

uniform vec2 u_resolution;
uniform mat3 u_transforms;

void main() {

    // Multiply the matrix by the vector, adding 1 to the vector to make
    // it the correct size. Keeping only x and y components.
    vec2 position = (u_transforms * vec3(a_position, 1)).xy;

    // Convert the position from pixels to 0.0 - 1.0
    vec2 zeroToOne = position / u_resolution;

    // Convert from 0->1 to 0->2
    vec2 zeroToTwo = zeroToOne * 2.0;

    // Convert from 0->2 to -1->1 (clip space)
    vec2 clipSpace = zeroToTwo - 1.0;

    // Invert Y axis
    //gl_Position = vec4(clipSpace[0], clipSpace[1] * -1.0, 0, 1);
    gl_Position = vec4(clipSpace * vec2(1, -1), 0, 1);
}
`;

const fsGLSL = `#version 300 es
precision highp float;

uniform vec4 u_color;

out vec4 outColor;

void main() {
    outColor = u_color;
}
`;

let objects = {
  model: {
    transforms: {
      // Transform in x,y and z component
      t: {
        x: 0,
        y: 0,
        z: 0,
      },
      // Rotation in radians
      rr: {
        x: 0,
        y: 0,
        z: 0,
      },
      // Scale
      s: {
        x: 1,
        y: 1,
        z: 1,
      },
    },
    color: [Math.random(), Math.random(), Math.random(), 1],
  },
};

function main() {
  const canvas = document.querySelector('canvas');
  const gl = canvas.getContext('webgl2');
  twgl.resizeCanvasToDisplaySize(gl.canvas);
  gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);


  const programInfo = twgl.createProgramInfo(gl, [vsGLSL, fsGLSL]);

  setupUI(gl);

  const arrays = shapeF();

  const bufferInfo = twgl.createBufferInfoFromArrays(gl, arrays);

  const vao = twgl.createVAOFromBufferInfo(gl, programInfo, bufferInfo);

  drawScene(gl, vao, programInfo, bufferInfo);
}

// Function to do the actual display of the objects
function drawScene(gl, vao, programInfo, bufferInfo) {
  // Translation
  let translate = [objects.model.transforms.t.x, objects.model.transforms.t.y];
  // Rotation
  let angles_radians = objects.model.transforms.rr.z;
  // Scale
  let scale = [objects.model.transforms.s.x, objects.model.transforms.s.y];
  // Create transform matrixes
  const scaMat = m3.scale(scale);
  const rotMat = m3.rotation(angles_radians);
  const traMat = m3.translation(translate);
  // Create a composite matrix
  let transforms = m3.identity();
  transforms = m3.multiply(scaMat, transforms);
  transforms = m3.multiply(rotMat, transforms);
  transforms = m3.multiply(traMat, transforms);

  let uniforms =
  {
    u_resolution: [gl.canvas.width, gl.canvas.height],
    u_transforms: transforms,
    u_color: objects.model.color,
  }

  gl.useProgram(programInfo.program);

  twgl.setUniforms(programInfo, uniforms);

  console.log(vao);

  gl.bindVertexArray(vao);

  twgl.drawBufferInfo(gl, bufferInfo);

  requestAnimationFrame(() => drawScene(gl, vao, programInfo, bufferInfo));
}

function setupUI(gl) {
  const gui = new GUI();

  const traFolder = gui.addFolder('Translation');
  // Translate model in x axis
  traFolder.add(objects.model.transforms.t, 'x', 0, gl.canvas.width)
  // Translate model in y axis
  traFolder.add(objects.model.transforms.t, 'y', 0, gl.canvas.height)
  const scaFolder = gui.addFolder('Scale');
  // Scale  model in x axis limit 3
  scaFolder.add(objects.model.transforms.s, 'x', 0, 3)
  // Scale model in y axis limit 3
  scaFolder.add(objects.model.transforms.s, 'y', 0, 3)
  // Rotate model
  const rotFolder = gui.addFolder('Rotation');
  rotFolder.add(objects.model.transforms.rr, 'z', 0, Math.PI * 2)

  // Change color
  gui.addColor(objects.model, 'color')
}

main()
