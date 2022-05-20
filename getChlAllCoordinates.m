
function chl_all = getChlAllCoordinates()

lat1 = [0 5 10 15 20 25 30 35 40 45 50 55];
lon = -30;
chl_all = [];
for lat = 1:length(lat1)
    sim = baserunWatercolumn(lat1(lat),lon);
    chl_all = [chl_all; sim.chl];
end
writematrix(chl_all,'/zhome/01/2/144033/Downloads/NUMmodel-main/chl_all_coordinates.csv');
end