import sys
import numpy as np
import torch
torch.set_num_threads(12)
torch.set_default_tensor_type('torch.FloatTensor')


def conv(nx, ny, nch, n, m, n_runs):

    # Turn off autograd
    with torch.no_grad():

        # Define convolution operator
        convt = torch.nn.Conv2d(nch, nch, (n, m), stride=(1, 1),
                                padding=(n//2, m//2), bias=False)

        # Image
        input_data = np.linspace(-1, 1, nx*ny*nch).reshape(1, nch, nx, ny)
        im_in = torch.from_numpy(input_data.astype(np.float32))

        # Weights
        ww = np.zeros((nch, nch, n, m), dtype=np.float32)
        for i in range(nch):
            ww[i, i, :, :] = np.linspace(i, i+(n*m), n*m).reshape(n, m).T

        # Popuate weights with deterministic values
        convt.weight[:] = torch.from_numpy(ww)

        # Applying convolution
        for j in range(n_runs):
            convt(im_in)


if __name__ == '__main__':

    k = int(sys.argv[1])
    n = 2**int(sys.argv[2])
    nch = 2**int(sys.argv[3])
    conv(n, n, nch, k, k, 50)
