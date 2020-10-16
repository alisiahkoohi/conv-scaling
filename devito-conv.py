import sys
import numpy as np
from devito import (SpaceDimension, Dimension, Grid, Function, Operator, Eq,
                    configuration)
configuration['log-level'] = 'WARNING'


def conv(nx, ny, nch, n, m, n_runs):

    # Image size
    dt = np.float32
    x, y, c = SpaceDimension("x"), SpaceDimension("y"), Dimension("c")
    grid = Grid((nch, nx, ny), dtype=dt, dimensions=(c, x, y))

    # Image
    im_in = Function(name="imi", grid=grid, space_order=n//2)
    input_data = np.linspace(-1, 1, nx*ny*nch).reshape(nch, nx, ny)
    im_in.data[:] = input_data.astype(np.float32)

    # Output
    im_out = Function(name="imo", grid=grid, space_order=n//2)
    im_out.data

    # Weights
    i, j = Dimension("i"), Dimension("j")
    W = Function(name="W", dimensions=(c, i, j), shape=(nch, n, m), grid=grid)

    # Popuate weights with deterministic values
    for i in range(nch):
        W.data[i, :, :] = np.linspace(i, i+(n*m), n*m).reshape(n, m)

    # Convlution
    conv = sum([W[c, i2, i1]*im_in[c, x+i1-n//2, y+i2-m//2]
                for i1 in range(n) for i2 in range(m)])

    # Applying convolution
    op = Operator(Eq(im_out, conv))
    for j in range(n_runs):
        op()


if __name__ == '__main__':

    k = int(sys.argv[1])
    n = 2**int(sys.argv[2])
    nch = 2**int(sys.argv[3])
    conv(n, n, nch, k, k, 50)
