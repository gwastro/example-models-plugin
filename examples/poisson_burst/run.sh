# create the data
python makedata.py
# now analyze it
pycbc_inference --config-file inference.ini \
    --output-file poisson_burst.hdf \
    --seed 20 \
    --verbose
