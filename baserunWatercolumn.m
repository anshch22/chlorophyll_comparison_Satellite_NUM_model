%
% Run a watercolumn with only generalists
%
% In:
%  lat, lon - latitude and longitude
%
% Out:
%  As simulation structure
%

function sim = baserunWatercolumn(lat,lon)

arguments
    lat double = 30;
    lon double = -30;
end


p = setupGeneralistsOnly(25);
p = parametersWatercolumn(p);
p.tEnd = 2*365;

sim = simulateWatercolumn(p, lat, lon);
sim.chl = getChl(sim);
disp(sim.dznom);
%-------------------------------
%plotSimulation(sim);
checkConservation(sim);
end