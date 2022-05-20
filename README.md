# chlorophyll_comparison_Satellite_NUM_model
Comparing chl-a concentration measured from satellite with NUM model simulated outputs

---- Add three files (baserunWatercolumn.m, getChl.m, getChlAllCoordinates.m) in NUM model


---- Please note that TMs are not available in this repository so MITgcm_ECCO has to be downloaded seperately and placed in TMs folder in matlab

1. To NUM model for all selected coordinates:
    run getChlAllCoordinates.m 

2. To NUM model for one selected coordinate:
    run baserunWatercolumn.m

3. To run comparison between satellite data and model output:
    run Sat_vs_NUM_model.py
