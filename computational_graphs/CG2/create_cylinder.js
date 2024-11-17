// Ricardo Alfredo Calvo Perez - A01028889
// 17/11/2024
// Create an .obj file to create a cylinder of n sides
// node create_cylinder.js [sides] [radius] [height]
// Function to create file

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function create_file(sides, radius, height, vertexes, faces, normals) {
  const outputDir = path.join(__dirname, 'OutputFiles'); // CurrentLocation/OutputFiles
  const fileName = `cylinder_s${sides}_r${radius}_h${height}.obj`; // Create name of new file by number of sides .obj
  const outputPath = path.join(outputDir, fileName); // Final directory with folder and new file CurrentLocation/OutputFiles/cylinder_${sides}.obj

  // If the file already exists overwrite content
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const content = `# Cylinder with ${sides} sides, radius ${radius}, height ${height}\n\n${vertexes.join('')}\n\n${normals.join('')}\n\n${faces.join('')}`;
  fs.writeFileSync(outputPath, content);
}

function get_normals(vec1, vec2, vec3) {
  const u = [
    vec2[0] - vec1[0],
    vec2[1] - vec1[1],
    vec2[2] - vec1[2],
  ];
  const v = [
    vec3[0] - vec1[0],
    vec3[1] - vec1[1],
    vec3[2] - vec1[2],
  ];

  const normal = [
    u[1] * v[2] - u[2] * v[1],
    u[2] * v[0] - u[0] * v[2],
    u[0] * v[1] - u[1] * v[0],
  ];
  return normal;
}

function calculate_vectors(sides, radius, heigh) {
  const v = []; // Vertexes
  const f = []; // Faces
  const vn = []; // Normal Vertexes
  const v_cords = []; // Normal Vertexes

  // z axis level
  const z = heigh / 2;
  // Central vertex from bottom
  v.push(`v ${"0".padStart(8)
    } ${"0".padStart(8)} ${(-z).toFixed(4).padStart(8)} \n`);

  v_cords.push([0, 0, (-z).toFixed(4).padStart(8)])
  // Central vertex from Top
  v.push(`v ${"0".padStart(8)} ${"0".padStart(8)} ${z.toFixed(4).padStart(8)} \n`);
  v_cords.push([0, 0, (z).toFixed(4).padStart(8)])


  // Get x and y axis for each side
  for (let i = 0; i < sides; i++) {
    // Find angle
    const angle = (2 * Math.PI) * (i / sides);
    const x = (radius * Math.cos(angle)).toFixed(4).padStart(8);
    const y = (radius * Math.sin(angle)).toFixed(4).padStart(8);


    // Add axis to array for the file
    // Bottom face
    v.push(`v ${x} ${y} ${(-z).toFixed(4).padStart(8)} \n`);
    v_cords.push([x, y, (-z).toFixed(4).padStart(8)])

    // Top face
    v.push(`v ${x} ${y} ${z.toFixed(4).padStart(8)} \n`);
    v_cords.push([x, y, (z).toFixed(4).padStart(8)])

  }
  console.log(v_cords);
  // Calculate bottom and top faces
  for (let index = 3; index < (sides * 2); index += 2) {
    // Bottom Face
    let normals = get_normals(v_cords[0], v_cords[index + 1], v_cords[index - 1]);
    vn.push(`vn ${(normals[0].toFixed(4).padStart(8))} ${(normals[1].toFixed(4).padStart(8))} ${(normals[2].toFixed(4).padStart(8))
      } \n`)
    f.push(`f 1//${vn.length} ${(index + 2)}//${vn.length} ${index}//${vn.length} \n`);

    // Top Face
    normals = get_normals(v_cords[1], v_cords[index + 1], v_cords[index - 1]);
    vn.push(`vn ${(normals[0].toFixed(4).padStart(8))} ${(normals[1].toFixed(4).padStart(8))} ${(normals[2].toFixed(4).padStart(8))
      } \n`)
    f.push(`f 2//${vn.length} ${(index + 1)}//${vn.length} ${index + 3}//${vn.length} \n`);


  }
  // Last Bottom and Top Triangles
  // Bottom Face
  let normals = get_normals(v_cords[0], v_cords[2], v_cords[(sides * 2)]);
  vn.push(`vn ${(normals[0].toFixed(4).padStart(8))} ${(normals[1].toFixed(4).padStart(8))} ${(normals[2].toFixed(4).padStart(8))
    } \n`)
  f.push(`f 1//${vn.length} 3//${vn.length} ${(sides * 2) + 1}//${vn.length} \n`);

  // Top Face
  normals = get_normals(v_cords[0], v_cords[2], v_cords[(sides * 2)]);
  vn.push(`vn ${(normals[0].toFixed(4).padStart(8))} ${(normals[1].toFixed(4).padStart(8))} ${(normals[2].toFixed(4).padStart(8))
    } \n`)
  f.push(`f 2//${vn.length} ${(sides * 2) + 2}//${vn.length} 4//${vn.length}\n`);

  // Lateral faces
  for (let vertex = 3; vertex < sides * 2; vertex += 2) {
    normals = get_normals(v_cords[vertex - 1], v_cords[vertex + 1], v_cords[vertex]);
    vn.push(`vn ${(normals[0].toFixed(4).padStart(8))} ${(normals[1].toFixed(4).padStart(8))} ${(normals[2].toFixed(4).padStart(8))
      } \n`)
    f.push(`f ${vertex}//${vn.length} ${vertex + 2}//${vn.length} ${vertex + 1}//${vn.length} \n`);

    normals = get_normals(v_cords[vertex + 2], v_cords[vertex], v_cords[vertex + 1]);
    vn.push(`vn ${(normals[0].toFixed(4).padStart(8))} ${(normals[1].toFixed(4).padStart(8))} ${(normals[2].toFixed(4).padStart(8))
      } \n`)
    f.push(`f ${vertex + 3}//${vn.length} ${vertex + 1}//${vn.length} ${vertex + 2}//${vn.length} \n`);
  }

  normals = get_normals(v_cords[(sides * 2)], v_cords[2], v_cords[(sides * 2) + 1]);
  vn.push(`vn ${(normals[0].toFixed(4).padStart(8))} ${(normals[1].toFixed(4).padStart(8))} ${(normals[2].toFixed(4).padStart(8))
    } \n`)
  f.push(`f ${(sides * 2) + 1}//${vn.length} 3//${vn.length} ${(sides * 2) + 2}//${vn.length} \n`);

  normals = get_normals(v_cords[3], v_cords[(sides * 2) + 1], v_cords[2]);
  vn.push(`vn ${(normals[0].toFixed(4).padStart(8))} ${(normals[1].toFixed(4).padStart(8))} ${(normals[2].toFixed(4).padStart(8))
    } \n`)
  f.push(`f 4//${vn.length} ${(sides * 2) + 2}//${vn.length} 3//${vn.length} \n`);

  create_file(sides, radius, heigh, v, f, vn)
}

function build_cylinder() {
  const sides = parseInt(process.argv[2]);
  const radius = parseFloat(process.argv[3]);
  const height = parseFloat(process.argv[4]);

  // Ask for sides
  if (isNaN(sides) || sides < 3 || sides > 360) {
    console.error("Invalid number of sides. Please enter a number between 3 and 360 as the first argument.");
    process.exit(1);
  }
  // Ask for radius
  if (isNaN(radius) || radius <= 0) {
    console.error("Invalid input for radius. Please enter a number 0.1 or higher as the second argument.");
    process.exit(1);
  }
  // Ask for heigh
  if (isNaN(height) || height <= 0) {
    console.error("Invalid input for height. Please enter a number 0.1 or higher as the third argument.");
    process.exit(1);
  }
  const animation = ["   ", ".", "..", "..."];
  let i = 0;

  const interval = setInterval(() => {
    process.stdout.write(`\rGenerating cylinder with ${sides} sides, radius ${radius}, and height ${height} ${animation[i % animation.length]} `);
    i++;
  }, 250); // new dot every 0.25 seconds

  setTimeout(() => {
    calculate_vectors(sides, radius, height); // Create file
    clearInterval(interval); // Stops animation
    // Over write with blanc spaces
    process.stdout.write(`\r`);
    console.log("\rFile creation completed!"); // Message when complete
  }, 4500); // Time of animation
}

build_cylinder();