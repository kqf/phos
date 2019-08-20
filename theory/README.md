## pQCD predictions for light hadron spectra

## Configuration
The INCNLO program input is limited only to 20 $p_T$ bins at once, therefore there are two separate configuration files `params.low.dat` and `params.high.dat` that correspond to low and high $p_T$ ranges. The parameters in those files are the same, only bin centers differ.

## How to run
The calculation runs inside docker container. Use the following command to automatically build the results
```
make
```
