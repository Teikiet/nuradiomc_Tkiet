"""
Simple, barebones simulation class

import NuRadioReco.modules.trigger.highLowThreshold
import NuRadioReco.modules.trigger.simpleThreshold
import NuRadioReco.modules.channelBandPassFilter
from NuRadioReco.utilities import units
from NuRadioMC.simulation import simulation

simple_threshold = simpleThreshold.triggerSimulator()


class Simulation(simulation.simulation):
    def _detector_simulation_filter_amp(self, evt, station, det):
        pass

    def _detector_simulation_trigger(self, evt, station, det):
        simple_threshold.run(
            evt=self._evt,
            station=self._station,
            det=self._det,
            threshold=4 * self._Vrms,
            number_concidences=3,
            trigger_name="simple_threshold",
        )


# initialize detector sim modules
simpleThreshold = NuRadioReco.modules.trigger.simpleThreshold.triggerSimulator()
highLowThreshold = NuRadioReco.modules.trigger.highLowThreshold.triggerSimulator()
channelBandPassFilter = NuRadioReco.modules.channelBandPassFilter.channelBandPassFilter()

class Simulation(simulation.simulation):

    def _detector_simulation_filter_amp(self, evt, station, det):
        channelBandPassFilter.run(evt, station, det, passband=[80 * units.MHz, 1000 * units.GHz],
                                  filter_type='butter', order=2)
        channelBandPassFilter.run(evt, station, det, passband=[0, 500 * units.MHz],
                                  filter_type='butter', order=10)

    def _detector_simulation_trigger(self, evt, station, det):
        # first run a simple threshold trigger
        simpleThreshold.run(evt, station, det,
                             threshold=3 * self._Vrms,
                             triggered_channels=None,  # run trigger on all channels
                             number_concidences=1,
                             trigger_name='simple_threshold')  # the name of the trigger

        # run a high/low trigger on the 4 downward pointing LPDAs
        highLowThreshold.run(evt, station, det,
                                    threshold_high=4 * self._Vrms,
                                    threshold_low=-4 * self._Vrms,
                                    triggered_channels=[0, 1, 2, 3],  # select the LPDA channels
                                    number_concidences=2,  # 2/4 majority logic
                                    trigger_name='LPDA_2of4_4.1sigma',
                                    set_not_triggered=(not station.has_triggered("simple_threshold")))  # calculate more time consuming ARIANNA trigger only if station passes simple trigger

        # run a high/low trigger on the 4 surface dipoles
        highLowThreshold.run(evt, station, det,
                                    threshold_high=3 * self._Vrms,
                                    threshold_low=-3 * self._Vrms,
                                    triggered_channels=[4, 5, 6, 7],  # select the bicone channels
                                    number_concidences=4,  # 4/4 majority logic
                                    trigger_name='surface_dipoles_4of4_3sigma',
                                    set_not_triggered=(not station.has_triggered("simple_threshold")))  # calculate more time consuming ARIANNA trigger only if station passes simple trigger
"""






import argparse
# import detector simulation modules
import NuRadioReco.modules.efieldToVoltageConverter
import NuRadioReco.modules.trigger.simpleThreshold
import NuRadioReco.modules.trigger.highLowThreshold
import NuRadioReco.modules.channelResampler
import NuRadioReco.modules.channelBandPassFilter
import NuRadioReco.modules.channelGenericNoiseAdder
from NuRadioReco.utilities import units
import numpy as np
from NuRadioMC.simulation import simulation
import matplotlib.pyplot as plt
import os


"""
    This file is a steering file that runs a simple NuRadioMC simulation. If one
    wants to run it with the default parameters, one just needs to type:

    python W02RunSimulation.py

    Otherwise, the arguments need to be specified as follows:

    python W02RunSimulation.py --inputfilename input.hdf5 --detectordescription detector.json
    --config config.yaml --outputfilename out.hdf5 --outputfilenameNuRadioReco out.nur

    The last argument is optional, only needed if the user wants a nur file. nur files
    contain lots of information on triggering events, so they're a great tool for
    reconstruction (see NuRadioReco documentation and Christoph's webinar). However,
    because of their massive amount of information, they can be really heavy. So, when
    running NuRadioMC with millions of events, most of the time nur files should not
    be created.

    Be sure to read the comments in the config.yaml file and also the file
    comments_detector.txt to understand how the detector.json function is structured.
    
    

    parser = argparse.ArgumentParser(description='Run NuRadioMC simulation')
    parser.add_argument('--inputfilename', type=str, default='input_3.2e+19_1.0e+20.hdf5',
                        help='path to NuRadioMC input event list')
    parser.add_argument('--detectordescription', type=str, default='detector.json',
                        help='path to file containing the detector description')
    parser.add_argument('--config', type=str, default='config.yaml',
                        help='NuRadioMC yaml config file')
    parser.add_argument('--outputfilename', type=str, default=os.path.join(results_folder, 'NuMC_output.hdf5'),
                        help='hdf5 output filename')
    parser.add_argument('--outputfilenameNuRadioReco', type=str, nargs='?', default=None,
                        help='outputfilename of NuRadioReco detector sim file')
    args = parser.parse_args()



    First we initialise the modules we are going to use. For our simulation, we are
    going to need the following ones, which are explained below.
"""
efieldToVoltageConverter = NuRadioReco.modules.efieldToVoltageConverter.efieldToVoltageConverter()
simpleThreshold = NuRadioReco.modules.trigger.simpleThreshold.triggerSimulator()
highLowThreshold = NuRadioReco.modules.trigger.highLowThreshold.triggerSimulator()
channelResampler = NuRadioReco.modules.channelResampler.channelResampler()
channelBandPassFilter = NuRadioReco.modules.channelBandPassFilter.channelBandPassFilter()
channelGenericNoiseAdder = NuRadioReco.modules.channelGenericNoiseAdder.channelGenericNoiseAdder()

"""
    A typical NuRadioMC simulation uses the simulation class from the simulation
    module. This class is incomplete by design, since it lacks the detector simulation
    functions that controls what the detector does after the electric field arrives
    at the antenna. That allows us to create our own class that inherits from
    the simulation class that we will call mySimulation, and define in it a
    _detector_simulation_filter_amp and _detector_simulation_trigger 
    function with all the characteristics of our detector setup.
"""


class Simulation(simulation.simulation):


    def _detector_simulation_filter_amp(self, evt, station, det):

        channelBandPassFilter.run(evt, station, det,
                                    passband=[1 * units.MHz, 700 * units.MHz], filter_type="butter", order=10)
        channelBandPassFilter.run(evt, station, det,
                                    passband=[150 * units.MHz, 800 * units.GHz], filter_type="butter", order=8)

    def _detector_simulation_trigger(self, evt, station, det):
        channel = list(np.linspace(0,15, 16))

        highLowThreshold.run(evt, station, det,
                                threshold_high=5 * self._Vrms,#originaly 1, 5 
                                threshold_low=-5 * self._Vrms,#originaly 1, 5
                                coinc_window=40 * units.ns,
                                triggered_channels=channel,
                                number_concidences=2,  # 2/4 majority logic
                                trigger_name='hilo_2of4_5_sigma')

        simpleThreshold.run(evt, station, det,
                                threshold=10 * self._Vrms, #originaly 10
                                triggered_channels=channel,
                                trigger_name='simple_10_sigma')


