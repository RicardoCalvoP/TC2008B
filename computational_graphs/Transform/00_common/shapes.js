/*
Function to create the vertex and color information for simple shapes
These can be used in multiple examples.

Gilberto Echeverria
2024-09-15
*/

// Create the data for the vertices of a polygon with the shape of the
// letter F. This is useful to view the transformations on the object.
function shapeF() {
    let arrays =
    {
        a_position: {
            numComponents: 2,
            data: [
                // Letter F
                0, 0,
                0, 200,
                40, 200,
                40, 0,
                40, 40,
                200, 40,
                200, 0,
                40, 120,
                150, 120,
                150, 80,
                40, 80,
            ]
        },
        indices: {
            numComponents: 3,
            data: [
                // Front face
                0, 1, 2,
                2, 3, 0,
                3, 4, 5,
                5, 6, 3,
                7, 8, 9,
                9, 10, 7,
            ]
        }
    };
    //console.log(arrays);

    return arrays;
}

// Create the data for a cube where each face has a different color
function cubeFaceColors(size) {
    let arrays = {
        a_position: {
            numComponents: 3,
            data: [
                // Front Face
                -1.0, -1.0, 1.0,
                1.0, -1.0, 1.0,
                1.0, 1.0, 1.0,
                -1.0, 1.0, 1.0,

                // Back face
                -1.0, -1.0, -1.0,
                -1.0, 1.0, -1.0,
                1.0, 1.0, -1.0,
                1.0, -1.0, -1.0,

                // Top face
                -1.0, 1.0, -1.0,
                -1.0, 1.0, 1.0,
                1.0, 1.0, 1.0,
                1.0, 1.0, -1.0,

                // Bottom face
                -1.0, -1.0, -1.0,
                1.0, -1.0, -1.0,
                1.0, -1.0, 1.0,
                -1.0, -1.0, 1.0,

                // Right face
                1.0, -1.0, -1.0,
                1.0, 1.0, -1.0,
                1.0, 1.0, 1.0,
                1.0, -1.0, 1.0,

                // Left face
                -1.0, -1.0, -1.0,
                -1.0, -1.0, 1.0,
                -1.0, 1.0, 1.0,
                -1.0, 1.0, -1.0
            ].map(e => size * e)
        },
        a_normal: {
            numComponents: 3,
            data: [
                // Front Face
                0, 0, 1,
                0, 0, 1,
                0, 0, 1,
                0, 0, 1,

                // Back face
                0, 0, -1,
                0, 0, -1,
                0, 0, -1,
                0, 0, -1,

                // Top face
                0, 1, 0,
                0, 1, 0,
                0, 1, 0,
                0, 1, 0,

                // Bottom face
                0, -1, 0,
                0, -1, 0,
                0, -1, 0,
                0, -1, 0,

                // Right face
                1, 0, 0,
                1, 0, 0,
                1, 0, 0,
                1, 0, 0,

                // Left face
                -1, 0, 0,
                -1, 0, 0,
                -1, 0, 0,
                -1, 0, 0,
            ]
        },
        a_color: {
            numComponents: 4,
            data: [
                // Front face
                1, 0, 0, 1, // v_1
                1, 0, 0, 1, // v_1
                1, 0, 0, 1, // v_1
                1, 0, 0, 1, // v_1
                // Back Face
                0, 1, 0, 1, // v_2
                0, 1, 0, 1, // v_2
                0, 1, 0, 1, // v_2
                0, 1, 0, 1, // v_2
                // Top Face
                0, 0, 1, 1, // v_3
                0, 0, 1, 1, // v_3
                0, 0, 1, 1, // v_3
                0, 0, 1, 1, // v_3
                // Bottom Face
                1, 1, 0, 1, // v_4
                1, 1, 0, 1, // v_4
                1, 1, 0, 1, // v_4
                1, 1, 0, 1, // v_4
                // Right Face
                0, 1, 1, 1, // v_5
                0, 1, 1, 1, // v_5
                0, 1, 1, 1, // v_5
                0, 1, 1, 1, // v_5
                // Left Face
                1, 0, 1, 1, // v_6
                1, 0, 1, 1, // v_6
                1, 0, 1, 1, // v_6
                1, 0, 1, 1, // v_6
            ]
        },
        indices: {
            numComponents: 3,
            data: [
                0, 1, 2, 0, 2, 3,    // Front face
                4, 5, 6, 4, 6, 7,    // Back face
                8, 9, 10, 8, 10, 11,  // Top face
                12, 13, 14, 12, 14, 15, // Bottom face
                16, 17, 18, 16, 18, 19, // Right face
                20, 21, 22, 20, 22, 23  // Left face
            ]
        }
    };

    return arrays;
}


// Create the data for a cube with each vertex in a different color
function cubeVertexColors(size) {
    let arrays =
    {
        a_position: {
            numComponents: 3,
            data: [
                1, 1, 1, // v_0
                1, -1, 1, // v_1
                -1, -1, 1, // v_2
                -1, 1, 1, // v_3
                1, 1, -1, // v_4
                1, -1, -1, // v_5
                -1, -1, -1, // v_6
                -1, 1, -1, // v_7
            ].map(e => size * e)
        },
        a_color: {
            numComponents: 4,
            data: [
                1, 1, 1, 1, // v_0
                1, 0, 0, 1, // v_1
                0, 1, 0, 1, // v_2
                0, 0, 1, 1, // v_3
                0, 0, 0, 1, // v_4
                1, 1, 0, 1, // v_5
                0, 1, 1, 1, // v_6
                1, 0, 1, 1, // v_7
            ]
        },
        indices: {
            numComponents: 3,
            data: [
                // Front face
                0, 2, 1,
                2, 0, 3,
                // Top face
                0, 5, 4,
                5, 0, 1,
                // Left face
                1, 6, 5,
                6, 1, 2,
                // Right face
                0, 7, 3,
                7, 0, 4,
                // Bottom face
                2, 7, 6,
                7, 2, 3,
                // Back face
                4, 6, 7,
                6, 4, 5,
            ]
        }
    };
    // console.log("ATTRIBUTES:")
    // console.log(arrays);

    return arrays;
}

function eightSidedWheel(size) {
    let arrays =
    {
        a_position: {
            numComponents: 3,
            data: [
                0, 0, 0,
                // Front Face
                0, 0, -0.5000,
                0, 0, 0.5000,
                5.0000, 0.0000, -0.5000,
                5.0000, 0.0000, 0.5000,
                3.5355, 3.5355, -0.5000,
                3.5355, 3.5355, 0.5000,
                0.0000, 5.0000, -0.5000,
                0.0000, 5.0000, 0.5000,
                - 3.5355, 3.5355, -0.5000,
                - 3.5355, 3.5355, 0.5000,
                - 5.0000, 0.0000, -0.5000,
                - 5.0000, 0.0000, 0.5000,
                - 3.5355, -3.5355, -0.5000,
                - 3.5355, -3.5355, 0.5000,
                - 0.0000, -5.0000, -0.5000,
                - 0.0000, -5.0000, 0.5000,
                3.5355, -3.5355, -0.5000,
                3.5355, -3.5355, 0.5000


            ].map(e => size * e)
        },
        a_color: {
            numComponents: 4,
            data: [
                // Front face
                1, 0, 0, 1, // v_1
                1, 0, 0, 1, // v_1
                1, 0, 0, 1, // v_1
                1, 0, 0, 1, // v_1
                // Back Face
                0, 1, 0, 1, // v_2
                0, 1, 0, 1, // v_2
                0, 1, 0, 1, // v_2
                0, 1, 0, 1, // v_2
                // Top Face
                0, 0, 1, 1, // v_3
                0, 0, 1, 1, // v_3
                0, 0, 1, 1, // v_3
                0, 0, 1, 1, // v_3
                // Bottom Face
                1, 1, 0, 1, // v_4
                1, 1, 0, 1, // v_4
                1, 1, 0, 1, // v_4
                1, 1, 0, 1, // v_4
                // Right Face
                0, 1, 1, 1, // v_5
                0, 1, 1, 1, // v_5
                0, 1, 1, 1, // v_5
                0, 1, 1, 1, // v_5
                // Left Face
                1, 0, 1, 1, // v_6
                1, 0, 1, 1, // v_6
                1, 0, 1, 1, // v_6
                1, 0, 1, 1, // v_6
            ]
        },
        indices: {
            numComponents: 3,
            data: [
                1, 5, 3,
                2, 4, 6,
                1, 7, 5,
                2, 6, 8,
                1, 9, 7,
                2, 8, 10,
                1, 11, 9,
                2, 10, 12,
                1, 13, 11,
                2, 12, 14,
                1, 15, 13,
                2, 14, 16,
                1, 17, 15,
                2, 16, 18,
                1, 3, 17,
                2, 18, 4,
                3, 5, 4,
                6, 4, 5,
                5, 7, 6,
                8, 6, 7,
                7, 9, 8,
                10, 8, 9,
                9, 11, 10,
                12, 10, 11,
                11, 13, 12,
                14, 12, 13,
                13, 15, 14,
                16, 14, 15,
                15, 17, 16,
                18, 16, 17,
                17, 3, 18,
                4, 18, 3,

            ]
        }
    };

    // console.log("ATTRIBUTES:")
    // console.log(arrays);

    return arrays;
}

export { shapeF, cubeFaceColors, cubeVertexColors, eightSidedWheel };
