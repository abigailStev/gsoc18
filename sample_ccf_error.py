## cs_array has been filtered before this step
cs_avg = np.mean(cs_array, axis=-1)

## Take the IFFT of the cross spectrum to get the CCF
ccf_avg = fftpack.ifft(cs_avg, axis=0).real
ccf_array = fftpack.ifft(cs_array, axis=0).real

## Apply normalization
ccv_avg *= (2.0 / np.float(n_bins) / ref_rms)
ccf_array *= (2.0 / np.float(n_bins) / ref_rms)

## Compute the standard error on each ccf bin from the segment-to-segment
## variations.
mean_ccf = np.mean(ccf_array, axis=2)
ccf_resid = (ccf_array.T - mean_ccf.T).T

## Eqn 2.3 from S. Vaughan 2013, "Scientific Inference"
sample_var = np.sum(ccf_resid**2, axis=2) / (meta_dict['n_seg'] - 1)

## Eqn 2.4 from S. Vaughan 2013, "Scientific Inference"
standard_error = np.sqrt(sample_var / meta_dict['n_seg'])

return ccf_avg, standard_error
