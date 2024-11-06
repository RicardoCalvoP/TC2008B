

const v2 = {
  crete: function (x, y) {
    let v = new Float32Array(2);
    v[0] = x;
    v[1] = y;
    return v;
  }
}

export const m3 = {
  identity: function () {
    return [
      1, 0, 0,
      0, 1, 0,
      0, 0, 1
    ];
  },

  translation: function (v) {
    return [
      1, 0, 0,
      0, 1, 0,
      v[0], v[1], 1
    ]
  },
  scale: function (v) {
    return [
      v[0], 0, 0,
      0, v[1], 0,
      0, 0, 1
    ];
  },
  rotation: function (angleRadians) {
    const c = Math.cos(angleRadians);
    const s = Math.sin(angleRadians);
    return [
      c, s, 0,
      -s, c, 0,
      0, 0, 1
    ];
  },
  multiply: function (ma, mb) {
    // Get individual elements of the matrices
    const ma00 = ma[0 * 3 + 0];
    const ma01 = ma[0 * 3 + 1];
    const ma02 = ma[0 * 3 + 2];
    const ma10 = ma[1 * 3 + 0];
    const ma11 = ma[1 * 3 + 1];
    const ma12 = ma[1 * 3 + 2];
    const ma20 = ma[2 * 3 + 0];
    const ma21 = ma[2 * 3 + 1];
    const ma22 = ma[2 * 3 + 2];

    const mb00 = mb[0 * 3 + 0];
    const mb01 = mb[0 * 3 + 1];
    const mb02 = mb[0 * 3 + 2];
    const mb10 = mb[1 * 3 + 0];
    const mb11 = mb[1 * 3 + 1];
    const mb12 = mb[1 * 3 + 2];
    const mb20 = mb[2 * 3 + 0];
    const mb21 = mb[2 * 3 + 1];
    const mb22 = mb[2 * 3 + 2];

    // Calculate each element in the resulting matrix
    return [
      ma00 * mb00 + ma10 * mb01 + ma20 * mb02,
      ma01 * mb00 + ma11 * mb01 + ma21 * mb02,
      ma02 * mb00 + ma12 * mb01 + ma22 * mb02,
      ma00 * mb10 + ma10 * mb11 + ma20 * mb12,
      ma01 * mb10 + ma11 * mb11 + ma21 * mb12,
      ma02 * mb10 + ma12 * mb11 + ma22 * mb12,
      ma00 * mb20 + ma10 * mb21 + ma20 * mb22,
      ma01 * mb20 + ma11 * mb21 + ma21 * mb22,
      ma02 * mb20 + ma12 * mb21 + ma22 * mb22,
    ]
  }

}