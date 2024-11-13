// Ricardo Alfredo Calvo Perez - A01028889
// 13/11/2024
// Create an .js file with the cylinder obj attributes
// node load_objs.js [path]

function load_obj(content) {

  const vertices = [0, 0, 0];
  const faces = [];

  const lines = content.split('\n');

  for (const line of lines) {
    const trimmedLine = line.trim();

    if (trimmedLine.startsWith('v ')) {

      const parts = trimmedLine.split(/\s+/).slice(1).map(parseFloat);
      vertices.push(...parts);
    } else if (trimmedLine.startsWith('f ')) {

      const parts = trimmedLine.split(/\s+/).slice(1).map(Number);
      faces.push(...parts);
    }
  }


  const arrays = {
    a_position: {
      numComponents: 3,
      data: vertices,
    },
    a_color: {
      numComponents: 4,
      data: [
        1.0, 1.0, 1.0, 1,
        0.9, 0.9, 0.9, 1,
        0.5, 0.5, 0.5, 1,
        0.2, 0.2, 0.2, 1,
        0.2, 0.2, 0.2, 1,
        0.5, 0.5, 0.5, 1,
        0.9, 0.9, 0.9, 1,
        1.0, 1.0, 1.0, 1,
      ],
    },

    indices: {
      numComponents: 3,
      data: faces,
    },
  };

  console.log(vertices);
  console.log(faces);
  return arrays;
}

export { load_obj }