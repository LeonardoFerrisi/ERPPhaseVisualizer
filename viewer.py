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


# ERPs

erp_offset = - 0.4
erp_offset2 = -0.2


def generate_left_erp():

    # Left Stimulus
    left_raw = np.sin((x-155)/amplitude_modifier) + erp_offset
    left_raw_2 = np.sin(x / amplitude_modifier) + erp_offset2

    # Component 1 - The N1 and P2
    comp1 =  left_raw[0:237] 
    # Component 2 - The P3
    comp2 = left_raw_2[237:322]

    left_erp =  np.concatenate((comp1, comp2, zeroes[0:678]))
    left_erp = left_erp + noise
    trace_left = go.Scatter(x=x, y=left_erp, name="Attend Left (Dominant)")

    return left_erp, trace_left




def generate_right_erp(offset=0):

  
    zerooffset = 0

    # Right Stimulus
    rightstim_modifer = 2
    right_raw = ( np.sin((x-(155))/amplitude_modifier) / rightstim_modifer ) # + erp_offset
    right_raw2 = ( np.sin(x / amplitude_modifier) / rightstim_modifer ) # + erp_offset2

    # Component1
    right_zero_comp = zeroes[0:zerooffset]
    r_comp1 = right_raw[zerooffset:237]
    right_comp1 = np.concatenate((right_zero_comp, r_comp1))

    # Component2 
    right_comp2 = right_raw2[237:330]
    
    z1 = zeroes[0:670-offset]
    z2 = zeroes[0:offset]

    right_erp = np.concatenate((z2, right_comp1, right_comp2, z1)) # starts at 0

    right_erp = right_erp + noise

    trace_right = go.Scatter(x=x, y=right_erp, name="Attend Right")

    return right_erp, trace_right




left_erp, trace_left = generate_left_erp()

right_erp, trace_right = generate_right_erp(offset=0)


trace_combo = go.Scatter(x=x, y=(left_erp + right_erp), name="Combo")


# Create a series of steps in steps of in 1ms incriments
steps = [dict(label='0 ms', method='update', args=[{'visible': [True, True]}, {'title': 'Frequency of: '}])]
for step in np.arange(0, 600, 1):


    combo = right_erp + left_erp

    right_erp, trace_right = generate_right_erp(offset=step)

    steps.append(dict(label=f'{step} ms', method='update', args=[{'y': [combo, left_erp, right_erp]}, {'title': f'Frequency of: {round(1000/step,4)} Hz'}]))

# Create a Plotly figure
fig = go.Figure(data=[trace_combo, trace_left, trace_right])

sliders = [dict(
        active = 1,
        steps = steps
    )]

fig.update_layout(
    sliders=sliders,
    title = 'Frequency of: ',
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