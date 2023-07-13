import NuRadioMC.EvtGen.NuRadioProposal as pp
from NuRadioReco.utilities import units, particle_names
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

container = pp.ProposalFunctions(config_file = "/home/tkiet/nuradiomc/test_secondary_ionization/config_PROPOSAL.json")

STAT = int(1e2)
energies = np.ones(STAT) * 1e13*units.MeV

codes_muon = np.empty(STAT, dtype=int)
codes_muon.fill(13)

codes_monopole = np.empty(STAT, dtype=int)
codes_monopole.fill(41)


secondaries_array_muons = container.get_secondaries_array(energies, codes_muon, propagate_decay_muons=False)

secondaries_array_monopoles = container.get_secondaries_array(energies, codes_monopole, propagate_decay_muons=False)

brems_list_muon = []
ioniz_list_muon = []
epair_list_muon = []
photonuclear_list_muon = []

brems_list_monopole = []
ioniz_list_monopole = []
epair_list_monopole = []
photonuclear_list_monopole = []


for secs in secondaries_array_muons:
    for s in secs:
        if (s.code == 81):
            brems_list_muon.append(s.energy)
        if (s.code == 82):
            ioniz_list_muon.append(s.energy)
        if (s.code == 83):
            epair_list_muon.append(s.energy)
        if (s.code == 85):
            photonuclear_list_muon.append(s.energy)
            
for secs in secondaries_array_monopoles:
    for s in secs:
        if (s.code == 81):
            brems_list_monopole.append(s.energy)
        if (s.code == 82):
            ioniz_list_monopole.append(s.energy)
        if (s.code == 83):
            epair_list_monopole.append(s.energy)
        if (s.code == 85):
            photonuclear_list_monopole.append(s.energy)            

bins = np.geomspace(1e15, 1e20, 10)

plt.figure(figsize=(8, 6), dpi=150)


plt.hist(epair_list_muon, bins=bins, histtype='step', label='epair', color='tab:blue')
plt.hist(ioniz_list_muon, bins=bins, histtype='step', label='ioniz', color='tab:green')
plt.hist(photonuclear_list_muon, bins=bins, histtype='step', label='nuclear', color='tab:orange')
plt.hist(brems_list_muon, bins=bins, histtype='step', label='brems', color='tab:red')

plt.legend()

plt.xscale('log')
plt.yscale('log')
plt.xlabel('E / MeV')
plt.title('Muon energy losses for NuRadioMC')
plt.show()
plt.savefig("Muon.pdf")

bins = np.geomspace(1e15, 1e20, 10)

plt.figure(figsize=(8, 6), dpi=150)


plt.hist(epair_list_monopole, bins=bins, histtype='step', label='epair', color='tab:blue')
plt.hist(ioniz_list_monopole, bins=bins, histtype='step', label='ioniz', color='tab:green')
plt.hist(photonuclear_list_monopole, bins=bins, histtype='step', label='nuclear', color='tab:orange')
plt.hist(brems_list_monopole, bins=bins, histtype='step', label='brems', color='tab:red')

plt.legend()

plt.xscale('log')
plt.yscale('log')
plt.xlabel('E / MeV')
plt.title('Monopole energy losses for NuRadioMC')
plt.show()
plt.savefig("monopole.pdf")

