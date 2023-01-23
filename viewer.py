import plotly.graph_objects as go
import numpy as np


# Generate x values
x = np.linspace(0, 600, 6000)

mod = 35
modA = mod * 2

ampMod = 1.0


sinA = np.sin(x/modA)/ampMod
# Create the first sine wave trace
trace1 = go.Scatter(x=x, y=sinA, name="Sine Wave 1")

# Create sine wave with 2000 samples
sine_wave = np.sin(np.linspace(0, 2 * np.pi, 2000))

# Create array of zeroes with 4000 samples
zeroes = np.zeros(4000)

# Join sine wave and zeroes using numpy.concatenate()
result = np.concatenate((sinA[0:2000], zeroes))

print(result.shape)


# Create the second sine wave trace
trace2 = go.Scatter(x=x, y=np.sin(x/mod), name="Sine Wave 2")

trace3 = go.Scatter(x=x, y=(np.sin(x/mod) - np.sin(x/mod)), name="Sine Wave 3")

# Create a series of steps in steps of 10s
steps = [dict(label='0 ms', method='update', args=[{'visible': [True, True]}, {'title': 'Step of 0 ms'}])]
for step in np.arange(0, 600, 5):

    # sin1 = np.sin(x/modA)/ampMod
    sin1 = np.concatenate((sinA[0:2000], zeroes))
    sin2 = np.sin((x-step)/mod)
    sin3 = sin1 + sin2
    steps.append(dict(label=f'{step} ms', method='update', args=[{'y': [sin1, sin2, sin3]}, {'title': f'Step of: {step} ms'}]))

# Create a Plotly figure
fig = go.Figure(data=[trace1, trace2, trace3])

sliders = [dict(
        active = 1,
        steps = steps
    )]

fig.update_layout(
    sliders=sliders,
    title = '0 ms',
    xaxis = dict(
        range = [0, 600],
        title = 'X'
    ),
    yaxis = dict(
        range = [-1.5, 1.5],
        title = 'Y'
    )
)

# Show the figure
fig.show()