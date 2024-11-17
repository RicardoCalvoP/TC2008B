/*
Ricardo Alfredo Calvo Perez - a01028889
17/11/2024


File to load all logic of matrixes in web gl
Pivot Object is shown as a red box
Main Object is shown as a green cylinder
 */


'use strict';

import * as twgl from 'twgl-base.js';
import GUI from 'lil-gui';
import { v3, m4 } from './libs/starter_3D_lib.js';

// Read the whole input file as a string
// https://vitejs.dev/guide/assets.html#importing-asset-as-string
// Define the shader code, using GLSL 3.00
import vsGLSL from './assets/shaders/vs_phong.glsl?raw';
import fsGLSL from './assets/shaders/fs_phong.glsl?raw';
import { load_obj } from './load_obj.js';
// import image from './OutputFiles/car.obj?raw'
import image from './OutputFiles/a01028889.obj?raw'
import pivot_Image from './OutputFiles/cube_normals.obj?raw'

// Variables used for the object, and coltrolled from the UI
const object = {
  model: {
    ambientColor: [0, 0.25, 0, 1.0],
    diffuseColor: [1, 1, 1, 1.0],
    specularColor: [0.3, 0.6, 0.6, 1.0],
    shininess: 100.0,
  },
  transforms: {
    // Translation
    t: {
      x: 5,
      y: 0,
      z: 0
    },
    // Rotation in degrees
    rd: {
      x: 0,
      y: 0,
      z: 0
    },
    // Rotation in radians
    rr: {
      x: 0,
      y: 0,
      z: 0
    },
    // Scale
    s: {
      x: 1,
      y: 1,
      z: 1
    },
    s_all: 1
  }
};

const pivot = {
  model: {
    ambientColor: [1, 0, 0, 1.0],
    diffuseColor: [1, 1, 1, 1.0],
    specularColor: [1, 0, 0, 1.0],
    shininess: 60.0,
  },
  transforms: {
    // Translation
    t: {
      x: -5,
      y: 0,
      z: 0
    },
    // Scale
    s: {
      x: 1,
      y: 1,
      z: 1
    },
  }
};

const settings = {
  // Speed in degrees
  rotationSpeed: {
    x: 0,
    y: 30,
    z: 0,
  },
  cameraPosition: {
    x: 0,
    y: 0,
    z: 10,
  },
  lightPosition: {
    x: 10,
    y: 10,
    z: 10,
  },
  ambientColor: [0.5, 0.5, 0.5, 1.0],
  diffuseColor: [0.5, 0.5, 0.5, 1.0],
  specularColor: [0.5, 0.5, 0.5, 1.0],
};

const duration = 1000; // ms
let then = 0;

let arrays = undefined;
let pivot_arrays = undefined;
let programInfo = undefined;
let vao = undefined;
let pivotVao = undefined;
let bufferInfo = undefined;
let pivotBufferInfo = undefined;

function setupWorldView(gl) {
  // Field of view of 60 degrees, in radians
  const fov = 60 * Math.PI / 180;
  const aspect = gl.canvas.clientWidth / gl.canvas.clientHeight;

  // Matrices for the world view
  const projectionMatrix = m4.perspective(fov, aspect, 1, 200);

  const cameraPosition = [settings.cameraPosition.x,
  settings.cameraPosition.y,
  settings.cameraPosition.z];
  const target = [0, 0, 0];
  const up = [0, 1, 0];
  const cameraMatrix = m4.lookAt(cameraPosition, target, up);

  const viewMatrix = m4.inverse(cameraMatrix);

  const viewProjectionMatrix = m4.multiply(projectionMatrix, viewMatrix);
  return viewProjectionMatrix;
}

// Function to do the actual display of the objects
function drawScene(gl) {
  // Compute time elapsed since last frame
  let now = Date.now();
  let deltaTime = now - then;
  const fract = deltaTime / duration;
  then = now;

  twgl.resizeCanvasToDisplaySize(gl.canvas);

  gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);

  // Clear the canvas
  gl.clearColor(0, 0, 0, 1);
  gl.enable(gl.DEPTH_TEST);
  gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

  // tell webgl to cull faces
  gl.enable(gl.CULL_FACE);

  // All objects will use the same program and vertices
  gl.useProgram(programInfo.program);

  const viewProjectionMatrix = setupWorldView(gl);

  // Convert the global transform values into twgl vectors

  // -----------------------------------
  // MAIN OBJECT TRANSFORMATIONS
  // -----------------------------------
  let mainObjectTransforms = v3.create(object.transforms.t.x,
    object.transforms.t.y,
    object.transforms.t.z);
  let mainObjectScale = v3.create(object.transforms.s.x,
    object.transforms.s.y,
    object.transforms.s.z);

  // Matrices for the object world transforms
  const mainMatrixTranslate = m4.translation(mainObjectTransforms);
  const mainMatrixRotationX = m4.rotationX(object.transforms.rr.x);
  const mainMatrixRotationY = m4.rotationY(object.transforms.rr.y);
  const mainMatrixRotationZ = m4.rotationZ(object.transforms.rr.z);
  const mainMatrixScale = m4.scale(mainObjectScale);

  // -----------------------------------
  // PIVOT OBJECT TRANSFORMATIONS
  // -----------------------------------
  let pivotTransforms = v3.create(pivot.transforms.t.x,
    pivot.transforms.t.y,
    pivot.transforms.t.z);

  let pivotInverseTransforms = v3.create(-pivot.transforms.t.x,
    -pivot.transforms.t.y,
    -pivot.transforms.t.z);

  let pivotScale = v3.create(pivot.transforms.s.x,
    pivot.transforms.s.y,
    pivot.transforms.s.z);

  const pivotMatrixTranslate = m4.translation(pivotTransforms);
  const pivotInverseMatrixTranslate = m4.translation(pivotInverseTransforms);
  const pivotMatrixScale = m4.scale(pivotScale);




  // Variable with the position of the light
  let v3_lightPosition = v3.create(settings.lightPosition.x,
    settings.lightPosition.y,
    settings.lightPosition.z);
  let v3_cameraPosition = v3.create(settings.cameraPosition.x,
    settings.cameraPosition.y,
    settings.cameraPosition.z);

  let globalUniforms = {
    u_viewWorldPosition: v3_cameraPosition,
    u_lightWorldPosition: v3_lightPosition,
    u_ambientLight: settings.ambientColor,
    u_diffuseLight: settings.diffuseColor,
    u_specularLight: settings.specularColor,
  };
  twgl.setUniforms(programInfo, globalUniforms);



  // -----------------------------------
  // MAIN OBJECT WORLD
  // -----------------------------------

  let world = m4.identity();
  world = m4.multiply(mainMatrixTranslate, pivotMatrixTranslate);
  world = m4.multiply(pivotInverseMatrixTranslate, world);
  world = m4.multiply(mainMatrixRotationX, world);
  world = m4.multiply(mainMatrixRotationY, world);
  world = m4.multiply(mainMatrixRotationZ, world);
  world = m4.multiply(pivotMatrixTranslate, world);
  world = m4.multiply(mainMatrixScale, world);


  let worldViewProjection = m4.multiply(viewProjectionMatrix, world);

  let transformsInverseTranspose = m4.identity();

  // -----------------------------------
  // PIVOT OBJECT WORLD
  // -----------------------------------

  let pivotWorld = m4.identity();
  pivotWorld = m4.multiply(pivotMatrixTranslate, pivotWorld);
  pivotWorld = m4.multiply(pivotMatrixScale, pivotWorld);

  let pivotWorldViewProjection = m4.multiply(viewProjectionMatrix, pivotWorld);
  let pivotTransformsInverseTranspose = m4.identity();

  // -----------------------------------
  // MAIN OBJECT UNIFORMS
  // -----------------------------------

  let modelUniforms = {
    u_transforms: worldViewProjection,

    u_world: world,
    u_worldInverseTransform: transformsInverseTranspose,
    u_worldViewProjection: worldViewProjection,
    u_ambientColor: object.model.ambientColor,
    u_diffuseColor: object.model.diffuseColor,
    u_specularColor: object.model.specularColor,
    u_shininess: object.model.shininess,
  }

  // -----------------------------------
  // PIVOT OBJECT UNIFORMS
  // -----------------------------------

  let pivotUniforms = {
    u_transforms: pivotWorldViewProjection,

    u_world: pivotWorld,
    u_worldInverseTransform: pivotTransformsInverseTranspose,
    u_worldViewProjection: pivotWorldViewProjection,
    u_ambientColor: pivot.model.ambientColor,
    u_diffuseColor: pivot.model.diffuseColor,
    u_specularColor: pivot.model.specularColor,
    u_shininess: pivot.model.shininess,

  }

  gl.bindVertexArray(vao);
  twgl.setUniforms(programInfo, modelUniforms);
  twgl.drawBufferInfo(gl, bufferInfo);

  gl.bindVertexArray(pivotVao);
  twgl.setUniforms(programInfo, pivotUniforms);
  twgl.drawBufferInfo(gl, pivotBufferInfo);



  requestAnimationFrame(() => drawScene(gl));
}

function setupUI(gl) {
  // Create the UI elements for each value
  const gui = new GUI();

  // Model controllers
  const modelFolder = gui.addFolder('Model:');
  modelFolder.addColor(object.model, 'ambientColor')
  modelFolder.addColor(object.model, 'diffuseColor')
  modelFolder.addColor(object.model, 'specularColor')
  modelFolder.add(object.model, 'shininess', 0, 600)
    .decimals(2)

  const transformsFolder = gui.addFolder('Transforms')
  const posFolder = transformsFolder.addFolder('Position:');
  posFolder.add(object.transforms.t, 'x', -5, 5)
    .decimals(2)
  posFolder.add(object.transforms.t, 'y', -5, 5)
    .decimals(2)
  posFolder.add(object.transforms.t, 'z', -5, 5)
    .decimals(2)
  const rotFolder = transformsFolder.addFolder('Rotation:');
  rotFolder.add(object.transforms.rd, 'x', 0, 360)
    .decimals(2)
    .listen()
    .onChange(value => {
      object.transforms.rd.x = value
      object.transforms.rr.x = object.transforms.rd.x * Math.PI / 180;
    });
  rotFolder.add(object.transforms.rd, 'y', 0, 360)
    .decimals(2)
    .listen()
    .onChange(value => {
      object.transforms.rd.y = value
      object.transforms.rr.y = object.transforms.rd.y * Math.PI / 180;
    });
  rotFolder.add(object.transforms.rd, 'z', 0, 360)
    .decimals(2)
    .listen()
    .onChange(value => {
      object.transforms.rd.z = value
      object.transforms.rr.z = object.transforms.rd.z * Math.PI / 180;
    });
  const scaFolder = transformsFolder.addFolder('Scale:');
  scaFolder.add(object.transforms, 's_all', -5, 5)
    .decimals(2)
    .onChange(value => {
      object.transforms.s.x = value;
      object.transforms.s.y = value;
      object.transforms.s.z = value;
    });
  scaFolder.add(object.transforms.s, 'x', -5, 5)
    .decimals(2)
    .listen()
  scaFolder.add(object.transforms.s, 'y', -5, 5)
    .decimals(2)
    .listen()
  scaFolder.add(object.transforms.s, 'z', -5, 5)
    .decimals(2)
    .listen()

  // Pivot Folder
  const pivot_Folder = gui.addFolder('Pivot: ')
  pivot_Folder.add(pivot.transforms.t, 'x', -5, 5)
    .decimals(2)
  pivot_Folder.add(pivot.transforms.t, 'y', -3, 3)
    .decimals(2)
  pivot_Folder.add(pivot.transforms.t, 'z', -5, 5)
    .decimals(2)

  // Settings for the animation
  const lightFolder = gui.addFolder('Light:')
  lightFolder.add(settings.lightPosition, 'x', -20, 20)
    .decimals(2)
  lightFolder.add(settings.lightPosition, 'y', -20, 20)
    .decimals(2)
  lightFolder.add(settings.lightPosition, 'z', -20, 20)
    .decimals(2)
  lightFolder.addColor(settings, 'ambientColor')
  lightFolder.addColor(settings, 'diffuseColor')
  lightFolder.addColor(settings, 'specularColor')
}

function main() {
  const canvas = document.querySelector('canvas');
  const gl = canvas.getContext('webgl2');

  setupUI(gl);

  programInfo = twgl.createProgramInfo(gl, [vsGLSL, fsGLSL]);

  // Set the default shape to be used
  arrays = load_obj(image); // Main Object Image
  pivot_arrays = load_obj(pivot_Image); // Pivot Object Image

  // Configure the Phong colors
  arrays.a_ambientColor = object.model.ambientColor;
  arrays.a_diffuseColor = object.model.diffuseColor;
  arrays.a_specularColor = object.model.specularColor;

  bufferInfo = twgl.createBufferInfoFromArrays(gl, arrays);
  vao = twgl.createVAOFromBufferInfo(gl, programInfo, bufferInfo);
  pivotBufferInfo = twgl.createBufferInfoFromArrays(gl, pivot_arrays);
  pivotVao = twgl.createVAOFromBufferInfo(gl, programInfo, pivotBufferInfo);






  drawScene(gl);
}

main()
