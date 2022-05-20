
function chl = getChl(sim)

%ixZ = 1;
ixT = 130;
Z = 10;
chl = [];
for ixZ = 1:Z
    B = sim.B(ixZ,:,ixT);
    L = sim.L(ixZ, ixT);
    u = [sim.N(ixZ, ixT), sim.DOC(ixZ, ixT), B];
    T = sim.T(ixZ,ixT);
    
    rates = getRates(sim.p, u, L, T);
    chl = [chl; sum(calcChl(B, rates, L))];
end

end

   