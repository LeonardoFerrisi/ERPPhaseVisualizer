import plotly.graph_objects as go
import numpy as np


"""
The following is based on Figure 3 from https://www.frontiersin.org/articles/10.3389/fnins.2012.00181/full 
(Communication and control by listening: toward optimal design of a two-class auditory streaming brain-computer interface).

This is a visualization tool for observing how two Event Related Potentials interact with variable spacing.

Leonardo Ferrisi
"""



# Generate x values
x = np.linspace(0, 1000, 1000)

amplitude_modifier = 35 # Scale to reduce amplitude of sine waves 



# Create array of zeroes with 4000 samples
zeroes = np.zeros(1000)


noise = np.random.normal(scale=0.009, size=zeroes.size)

SIGNAL_PERIOD = 322
FULL_PERIOD = 1000

P2_2_P3_SAMPLE = 240

SIGNAL_OFFSET = 155

# ERPs

erp_offset = - 0.4
erp_offset2 = -0.2


def generate_left_erp():

    offset = 30
    # Left Stimulus
    left_raw = np.sin((x-SIGNAL_OFFSET)/amplitude_modifier) + erp_offset
    left_raw_2 = np.sin(x / amplitude_modifier) + erp_offset2

    # Component 1 - The N1 and P2
    z_start = zeroes[0:offset]
    comp1 =  np.concatenate((z_start,left_raw[offset:P2_2_P3_SAMPLE]))
    # Component 2 - The P3
    comp2 = left_raw_2[P2_2_P3_SAMPLE:SIGNAL_PERIOD]

    left_erp =  np.concatenate((comp1, comp2, zeroes[0:FULL_PERIOD-SIGNAL_PERIOD]))
    #left_erp -= left_erp.flat[0]
    left_erp = left_erp + noise
    trace_left = go.Scatter(x=x, y=left_erp, name="Response to Left Stimuli (Attended)")

    return left_erp, trace_left




def generate_right_erp(offset=0):

  
    zerooffset = 39
    right_sig_inital_zeros = 44

    # Right Stimulus
    rightstim_modifer = 2
    right_raw = ( np.sin((x-((SIGNAL_OFFSET+zerooffset)-right_sig_inital_zeros))/amplitude_modifier) / rightstim_modifer ) # + erp_offset
    right_raw2 = ( np.sin(x / amplitude_modifier) / rightstim_modifer ) # + erp_offset2

    # Component1
    right_zero_comp = zeroes[0:zerooffset]
    r_comp1 = right_raw[zerooffset:P2_2_P3_SAMPLE]
    right_comp1 = np.concatenate((right_zero_comp, r_comp1))

    # Component2 
    right_comp2 = right_raw2[P2_2_P3_SAMPLE:SIGNAL_PERIOD]
    
    z1 = zeroes[0:(FULL_PERIOD-SIGNAL_PERIOD)-offset]
    z2 = zeroes[0:offset]

    right_erp = np.concatenate((z2, right_comp1, right_comp2, z1)) # starts at 0
    #right_erp -= right_erp.flat[0]
    right_erp = right_erp + noise

    trace_right = go.Scatter(x=x, y=right_erp, name="Response to Right Stimuli")

    return right_erp, trace_right




left_erp, trace_left = generate_left_erp()

right_erp, trace_right = generate_right_erp(offset=0)


trace_combo = go.Scatter(x=x, y=(left_erp + right_erp), name="Combo")



# Create a series of steps in steps of in 1ms incriments
steps = [dict(label='0 ms', method='update', args=[{'visible': [True, True]}, {'title': 'Move slider to align right'}])]
for offset in np.arange(1, 601, 1):


    

    
    

    freq_per_stream = round(1000/(offset*2),4)
    freq_bt_streams = round(1000/offset, 4)

    next_left_start_idx = None
    next_right_start_idx = None

    # For the offset, append a copy of the erp after the offset and crop it to fit 1000ms / 1000 samples 
    if (offset*2) > SIGNAL_PERIOD:
        # make another left
        next_left = left_erp

        next_left_start_idx = offset*2
        next_left_end_idx = (offset*2)+SIGNAL_PERIOD

        if next_left_start_idx < FULL_PERIOD:
            
            # if next_left_end_idx <= FULL_PERIOD:
            # print(f"Next left end: {next_left_end_idx}")
            z = zeroes[0: ( (FULL_PERIOD) - ( next_left_end_idx )) ]
            # print(f"Zero size = {z.size}")
            next_left_temp = np.concatenate(( next_left[0:SIGNAL_PERIOD], z ))

            l = np.concatenate(( left_erp[0: (offset*2)], next_left ))
            left_erp = l[0:FULL_PERIOD]

    right_erp, trace_right = generate_right_erp(offset=offset)


    # # For the right one
    # if (offset*3) > (offset+SIGNAL_PERIOD):
    #     next_right = right_erp
    #     next_right_start_idx = offset*3
    #     next_right_end_idx = (offset*3)+SIGNAL_PERIOD

    #     if next_right_start_idx < FULL_PERIOD:
            
    #         if next_right_end_idx <= FULL_PERIOD:
    #             # print(f"Next r end: {next_right_end_idx}")
    #             z = zeroes[0: ( (FULL_PERIOD) - ( next_right_end_idx )) ]
    #             # print(f"Zero size = {z.size}")
    #             next_right_temp = np.concatenate(( next_right[0:SIGNAL_PERIOD], z ))

    #             r = np.concatenate(( right_erp[0: next_right_start_idx], next_right_temp ))
    #             right_erp = r[0:FULL_PERIOD]
    
    print(f"Offset: {offset}, Next Left starts at: {next_left_start_idx}, Next Right starts at: {next_right_start_idx}")



  

    # print(f"For offset: {offset}, Next Left: {next_left_start_index}")


    # next_right_start_index = (offset)
     

    
    combo = left_erp - right_erp # using Subtraction as opposed to sum

    steps.append(dict(label=f'Between Stream Period: {offset} ms', method='update', args=[{'y': [combo, left_erp, right_erp]}, {'title': f'Between Stream Period of: {offset} ms | Within Stream Period of: {offset*2} ms | Frequency of: {freq_per_stream} Hz per stream | Frequency of: {freq_bt_streams} Hz between streams'}]))

# Create a Plotly figure
fig = go.Figure(data=[trace_combo, trace_left, trace_right])

sliders = [dict(
        active = 1,
        steps = steps
    )]

fig.update_layout(
    sliders=sliders,
    title = 'Move slider to align right response',
    xaxis = dict(
        range = [0, 1000],
        title = 'Time (ms)'
    ),
    yaxis = dict(
        range = [-1.5, 1.5],
        title = 'Amplitude (uV)'
    )
)

# Show the figure
fig.show()