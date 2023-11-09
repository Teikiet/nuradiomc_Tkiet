import ROOT 
import numpy as np
import matplotlib.pyplot as plt
import radiotools.helper
import scipy
import re
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import h5py
import glob 
from scipy import interpolate
import json
import os
import sys
from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from math import isclose
import mplhep as hep
from scipy.signal import find_peaks

def correlation(channel1, channel2):
    return radiotools.helper.get_normalized_xcorr(channel1,channel2)
def correlation2(trace1, trace2):
    return scipy.signal.correlate(trace1, trace2, mode='full', method='auto') / (np.sum(trace1 ** 2) * np.sum(trace2 ** 2)) ** 0.5

# Loop through the keys and identify TGraph objects

def get_channel_name(file):
    root_file = ROOT.TFile(file, "READ")
    keys = root_file.GetListOfKeys()
    G_name = []
    for key in keys:
        obj = key.ReadObj()
        if isinstance(obj, ROOT.TGraph):
            graph_name = key.GetName()
            G_name.append(graph_name)

    v_pole_channel_name = []
    h_pole_channel_name = []
    for i in range(len(G_name)):
        test_string = (G_name[i][-2:])
        temp = re.findall(r'\d+', test_string)
        temp = int(temp[0])
        if temp <= 7:
            v_pole_channel_name.append(G_name[i])
        else:
            h_pole_channel_name.append(G_name[i])
    return v_pole_channel_name, h_pole_channel_name

def read_root_file(root_file, graph_name):
    root_file = ROOT.TFile(root_file, "READ")
    # Get the TGraph by name
    graph = root_file.Get(graph_name)
    test_string = (graph_name[-2:])
    temp = re.findall(r'\d+', test_string)
    channel_id = int(temp[0])

    test_string = (graph_name[0:9])
    event_id = test_string
    # Check if the TGraph exists
    if graph:
        # Access information about the TGraph
        n_points = graph.GetN()

        # Convert LowLevelViews to Python lists
        #x_values = np.frombuffer(graph.GetX(), dtype=np.float64)
        y_values = np.frombuffer(graph.GetY(), dtype=np.float64)
        return event_id, channel_id, y_values
    else:
        print("TGraph", graph_name, "not found in the ROOT file.")
    root_file.Close()
# Close the ROOT file when done

#Get data:
def get_trace_from_root(root_file, G_name):
    data = []
    event_id = 1
    event_name = read_root_file(root_file, G_name[0])[0]
    for i in range(len(G_name)):
        data_i = []
        if event_name != read_root_file(root_file, G_name[i])[0]:
            event_id += 1
            event_name = read_root_file(root_file, G_name[i])[0]
        channel_name = read_root_file(root_file, G_name[i])[1]
        trace = read_root_file(root_file, G_name[i])[2]
        data_i.append(event_id)
        data_i.append(channel_name)
        data_i.append(trace)
        data.append(data_i)
    return data

def RPR(trace):
    num_subarrays = int(len(trace)/40)
    subarrays = np.array_split(trace, num_subarrays)
    power_values = np.array([np.sqrt(1/len(subarray) * sum(subarray**2)) for subarray in subarrays])
    max_power = max(power_values)
    index = np.where(power_values != max_power)
    power_values = power_values[index]
    rms = np.sqrt(sum(power_values**2)/len(power_values))
    return max_power/rms

def get_correlation_between_channel(data_trace_1, data_trace_2):
    event = []
    rpr = []
    corr = []
    if data_trace_1 == data_trace_2 and len(data_trace_1[0]) == 5:
        for i in range(len(data_trace_1)):
            for j in range(i+1, len(data_trace_2)):
                event1 = data_trace_1[i][4]
                event2 = data_trace_2[j][4]

                station1 = data_trace_1[i][1]
                station2 = data_trace_2[j][1]
                
                if station1 == station2 and event1 == event2:
                    trace_1 = data_trace_1[i][3]
                    trace_2 = data_trace_2[j][3]
                    if sum(trace_1) != 0 and sum(trace_2) != 0:
                        event_i = event1
                        rpr_i = max(RPR(trace_1), RPR(trace_2))
                        corr_i =max(correlation(np.array(trace_1), np.array(trace_2)))
                        event.append(event_i)
                        rpr.append(rpr_i)
                        corr.append(corr_i)
    elif len(data_trace_1[0]) == 3:
        for i in range(len(data_trace_1)):
            for j in range(i+1, len(data_trace_2)):
                event_i = data_trace_1[i][0]
                channel1 = data_trace_1[i][1]
                channel2 = data_trace_2[j][1]
                if channel1 != channel2:
                    trace_1 = data_trace_1[i][2]
                    trace_2 = data_trace_2[j][2]
                    event.append(event_i)
                    rpr_i = max(RPR(trace_1), RPR(trace_2))
                    corr_i = max(correlation(np.array(trace_1), np.array(trace_2)))
                    rpr.append(rpr_i)
                    corr.append(corr_i)
    return event, rpr, corr

def get_list_peak(trace_data):
    P = [trace_data[i][0] for i in range(len(trace_data))]
    max_P = max(P)
    list_P = np.arange(0, max_P+1)
    list_P = list(list_P)
    return list_P

def get_mean_error(event, rpr, corr):
    mean_CORR = []
    err_CORR = []
    mean_RPR = []
    err_RPR = []

    EVENT = []

    corr_i = []
    rpr_i = []
    event_i = event[0]
    i = 0
    while i < len(event):
        if event[i] == event_i:
            event_i = event[i]
            corr_i.append(corr[i])
            rpr_i.append(rpr[i])
        else:
            mean_CORR.append(np.mean(corr_i))
            err_CORR.append(stats.sem(corr_i))
            mean_RPR.append(np.mean(rpr_i))
            err_RPR.append(stats.sem(rpr_i))
            EVENT.append(event_i)
            corr_i = []
            rpr_i = []
            event_i = event[i]
        i += 1
    return EVENT, mean_CORR, err_CORR, mean_RPR, err_RPR   



# data in csv file:
file_8074 = "/home/tkiet/fBC_TGraphs_run8074.root"
file_A3 = "/home/tkiet/fBC_TGraphs_A3.root"
file_a = "/home/tkiet/a.root"    

file_a = file_8074
v_pole_channel_name_a, h_pole_channel_name_a = get_channel_name(file_a)
data_a = get_trace_from_root(file_a, v_pole_channel_name_a)
event_a, rpr_a, corr_a = get_correlation_between_channel(data_a, data_a)
EVENT_a, mean_CORR_a, err_CORR_a, mean_RPR_a, err_RPR_a = get_mean_error(event_a, rpr_a, corr_a)

#Save data to csv file:
data = np.array([EVENT_a, mean_CORR_a, err_CORR_a, mean_RPR_a, err_RPR_a])
data = np.transpose(data)
df = pd.DataFrame(data, columns=["event", "mean_CORR", "err_CORR", "mean_RPR", "err_RPR"])
df.to_csv("data_a.csv", index=False)