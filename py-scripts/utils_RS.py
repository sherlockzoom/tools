def stretch_8bit(bands, lower_percent=2, higher_percent=98):
    # print(bands.shape)
    out = np.zeros_like(bands).astype(np.uint8)
    # for i in range(3):
    a = 0
    b = 255
    c = np.percentile(bands, lower_percent)
    d = np.percentile(bands, higher_percent)
    t = a + (bands - c) * (b - a) / (d - c)
    t[t<a] = a
    t[t>b] = b
    out[:,:] =t
    return out.astype(np.uint8)
