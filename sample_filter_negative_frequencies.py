## Filtering by a window function on the FWHM of the QPO (QPO is at 5.7 Hz)

## Finding the index in the frequency array of the window's lower bound
lf = int(find_nearest(freq[0:int(n_bins/2+1)], 4.28)[1])
## Finding the index in the frequency array of the window's higher bound
hf = int(find_nearest(freq[0:int(n_bins/2+1)], 7.13)[1])

## The window function of the positive frequencies.
## There are zeros before the window we want, ones for the window,
## and zeros after the window up to the nyquist frequency at index n_bins/2+1
## For scipy fft, the nyquist frequency is given a negative sign and is at n_bins/2+1
## Their example here: https://docs.scipy.org/doc/scipy/reference/generated/scipy.fftpack.fft.html
## 4 is their nyquist frequency, and it can be positive or negative in sign
pf_window = np.concatenate((np.zeros(lf, dtype=np.complex128),
                            np.ones(hf - lf, dtype=np.complex128),
                            np.zeros(int(n_bins/2+1) - hf,
                                     dtype=np.complex128)))
## This is the window function for the negative Fourier frequencies
nf_window = pf_window[1:-1]

## Here's the whole filter together. It has length n_bins.
## Note that the negative one is flipped/mirrored by [::-1]
qpo_filter = np.concatenate((pf_window, nf_window[::-1]))



# Here's the find_nearest array I use above. Might not be needed for your implementation
def find_nearest(array, value):
    """
    Thanks StackOverflow!

    Parameters
    ----------
    array : np.array of ints or floats
        1-D array of numbers to search through. Should already be sorted
        from low values to high values.

    value : int or float
        The value you want to find the closest to in the array.

    Returns
    -------
    array[idx] : int or float
        The array value that is closest to the input value.

    idx : int
        The index of the array of the closest value.
    """
    idx = np.searchsorted(array, value, side="left")
    if idx == len(array) or np.fabs(value - array[idx - 1]) < \
        np.fabs(value - array[idx]):
        return array[idx - 1], idx - 1
    else:
        return array[idx], idx
