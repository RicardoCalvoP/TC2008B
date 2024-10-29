// Ricardo Alfredo Calvo Perez - A01028889
// Create an obj file of an cylinder

const fs = require('fs');
const path = require('path');

const sides = parseInt(process.argv[2]);

function build_cylinder(params) {

}

function create_file(sides) {
  const outputDir = path.join(__dirname, 'output_files');
  const fileName = `cylinder_${sides}.obj`;
  const outputPath = path.join(outputDir, fileName);

  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  fs.writeFileSync(outputPath, fileName);
  console.log(`File created at: ${outputPath}`);
}



if (isNaN(sides) || sides < 3 || sides > 360) {
  console.error("Invalid number of sides. Please enter a number between 3 and 360 as a command argument.");
  process.exit(1);
}

console.log(`Creating cylinder with ${sides} sides...`);

create_file(sides);
