

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
    // Get components of matrix ma
    const ma00 = ma[0 * 3 + 0], ma01 = ma[0 * 3 + 1], ma02 = ma[0 * 3 + 2];
    const ma10 = ma[1 * 3 + 0], ma11 = ma[1 * 3 + 1], ma12 = ma[1 * 3 + 2];
    const ma20 = ma[2 * 3 + 0], ma21 = ma[2 * 3 + 1], ma22 = ma[2 * 3 + 2];

    // Get components of matrix mb
    const mb00 = mb[0 * 3 + 0], mb01 = mb[0 * 3 + 1], mb02 = mb[0 * 3 + 2];
    const mb10 = mb[1 * 3 + 0], mb11 = mb[1 * 3 + 1], mb12 = mb[1 * 3 + 2];
    const mb20 = mb[2 * 3 + 0], mb21 = mb[2 * 3 + 1], mb22 = mb[2 * 3 + 2];

    // Calculate each element in the resulting matrix
    return [
      ma00 * mb00 + ma01 * mb10 + ma02 * mb20,
      ma00 * mb01 + ma01 * mb11 + ma02 * mb21,
      ma00 * mb02 + ma01 * mb12 + ma02 * mb22,

      ma10 * mb00 + ma11 * mb10 + ma12 * mb20,
      ma10 * mb01 + ma11 * mb11 + ma12 * mb21,
      ma10 * mb02 + ma11 * mb12 + ma12 * mb22,

      ma20 * mb00 + ma21 * mb10 + ma22 * mb20,
      ma20 * mb01 + ma21 * mb11 + ma22 * mb21,
      ma20 * mb02 + ma21 * mb12 + ma22 * mb22
    ];
  }

}