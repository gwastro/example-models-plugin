pycbc_inference_plot_posterior \
    --input-file poisson_burst.hdf \
    --output-file posterior-possion_burst.png \
    --plot-marginal --plot-scatter --z-arg loglikelihood \
    --plot-contours --max-kde-samples 5000 \
    --expected-parameters amp:24 tau:4.0 \
    --verbose
