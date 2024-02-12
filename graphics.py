import matplotlib.pyplot as plt
import numpy as np

from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections import register_projection
from matplotlib.projections.polar import PolarAxes
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D


def radar_factory(num_vars, frame='circle'):
    """
    Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle', 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarTransform(PolarAxes.PolarTransform):

        def transform_path_non_affine(self, path):
            # Paths with non-unit interpolation steps correspond to gridlines,
            # in which case we force interpolation (to defeat PolarTransform's
            # auto conversion to circular arcs).
            if path._interpolation_steps > 1:
                path = path.interpolated(num_vars)
            return Path(self.transform(path.vertices), path.codes)

    class RadarAxes(PolarAxes):
        name = 'radar'
        PolarTransform = RadarTransform

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self.__close_line__(line)

        @staticmethod
        def __close_line__(line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def set_varlabels(self, labels):
            new_theta = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
            self.set_thetagrids(np.degrees(new_theta), labels)

        @staticmethod
        def __gen_axes_patch__():
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def __gen_axes_spines__(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta


def example_data():
    # data = [
    #     ['RDA-F1-01M', 'RDA-F1-01D', 'RDA-F1-02M', 'RDA-F1-02D', 'RDA-F2-01M', 'RDA-F3-01M', 'RDA-F4-01M'],
    #     ('Findable', [
    #         [1, 2, 3, 4, 0, 2, 3]]),
    #     ('Accessible', [
    #         [1, 2, 3, 4, 0, 2, 3]]),
    #     ('Interoperable', [
    #         [1, 2, 3, 4, 0, 2, 3]]),
    #     ('Reusable', [
    #         [1, 2, 3, 4, 0, 2, 3]])
    # ]
    






    data = {
        'Findable': {
            'labels': ['RDA-F1-01M', 'RDA-F1-01D', 'RDA-F1-02M', 'RDA-F1-02D', 'RDA-F2-01M', 'RDA-F3-01M',
                       'RDA-F4-01M'],
            'data': [1, 2, 3, 4, 1, 2, 3]
        },
        'Accessible': {
            'labels': ['RDA-A1-01M', 'RDA-A1-02M', 'RDA-A1-02D', 'RDA-A1-03M', 'RDA-A1-03D', 'RDA-A1-04M',
                       'RDA-A1-04D', 'RDA-A1-05D', 'RDA-A1.1-01M', 'RDA-A1.1-01D', 'RDA-A1.2-01D', 'RDA-A2-01M' ],
            'data': [1, 2, 3, 4, 5, 2, 3, 4, 3, 2, 1, 1]
        },
        'Interoperable': {
            'labels': ['RDA-I1-01M', 'RDA-I1-01D', 'RDA-I1-02M', 'RDA-I1-02D', 'RDA-I2-01M', 'RDA-I2-01D',
                       'RDA-I3-01M', 'RDA-I3-01D', 'RDA-I3-02M', 'RDA-I3-02D', 'RDA-I3-03M', 'RDA-I3-04M'],
            'data': [1, 2, 3, 4, 5, 2, 3, 3, 1, 2, 1, 5]
        },
        'Reusable': {
            'labels': ['RDA-R1-01M', 'RDA-R1.1-01M', 'RDA-R1.1-02M', 'RDA-R1.1-03M', 'RDA-R1.2-01M',
                       'RDA-R1.2-02M', 'RDA-R1.3-01M', 'RDA-R1.3-01D', 'RDA-R1.3-02M', 'RDA-R1.3-02D'],
            'data': [1, 2, 3, 4, 5, 2, 3, 1, 1, 2]
        }
    }

    return data


def create_first_figure():
    data = example_data()

    theta = {
        'Findable': radar_factory(num_vars=len(data['Findable']['labels']), frame='polygon'),
        'Accessible': radar_factory(num_vars=len(data['Accessible']['labels']), frame='polygon'),
        'Interoperable': radar_factory(num_vars=len(data['Interoperable']['labels']), frame='polygon'),
        'Reusable': radar_factory(num_vars=len(data['Reusable']['labels']), frame='polygon')
    }

    # Create the first radar chart in Figure 1
    fig, axs = plt.subplots(figsize=(9, 9), nrows=2, ncols=2, subplot_kw=dict(projection='radar'))

    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

    zipped = [[array_element, key, value] for array_element, (key, value) in zip(axs.flat, data.items())]
    i = 0
    # axs = axs.flat
    # Plot the four cases from the example data on separate axes
    for ax, key, value in zipped:
        ax.set_rgrids([1, 2, 3, 4, 5])
        ax.set_title(label=key,
                     weight='bold',
                     size='large',
                     position=(0.5, 1.1),
                     horizontalalignment='center',
                     verticalalignment='center',
                     pad=20,
                     fontsize=16)

        ax.plot(theta[key], value['data'], color='#48BADD')
        ax.fill(theta[key], value['data'], facecolor='#48BADD', alpha=0.25, label='_nolegend_')
        ax.set_varlabels(value['labels'])
        ax.tick_params(axis='x', pad=15)

    fig.text(0.5, 0.965, 'FAIRNESS Progress per Indicator',
             horizontalalignment='center', color='black', weight='bold',
             fontsize=18)

    # Adjust the spacing between subplots
    plt.subplots_adjust(wspace=0.5, hspace=0.5)


def create_second_figure():
    import matplotlib.pyplot as plt
    import numpy as np

    # Create the color map from white to blue
    cmap = plt.cm.get_cmap('Blues')

    # Set the number of divisions in each column
    num_divisions = 6

    # Create the figure and axes
    fig, ax = plt.subplots()

    # Set the width of each column
    column_width = 0.6

    # Set the distance between the columns
    column_distance = 0.8

    # Iterate over each column
    for i in range(4):
        # Calculate the x-coordinate of the column
        x = i * (column_width + column_distance)

        # Iterate over each division within the column
        for j in range(num_divisions):
            # Calculate the color value for the division
            color_value = j / (num_divisions - 1)

            # Get the color for the division using the color map
            color = cmap(color_value)

            # Plot the bar for the division
            ax.bar(x, 1, bottom=j, color=color, edgecolor='none', width=column_width)

    # Add white lines at the top of each division within the column
    y = (num_divisions - 1) + 0.5 - 0.02  # the lines have linewidht=3, so to center the line we need to rest 0.01
    # TODO: need to calculate -0.1 in function of the dimensions of the case, 0.1 is = -0.1 + 0.2 (extension of the line)
    x1, y1 = [-0.07, 0.07], [y, y]
    inc_x = [column_width+column_distance, column_width+column_distance]
    for i in range(num_divisions):
        plt.plot(x1, y1, color="white", linewidth=4)
        x1, y1 = [x1[i] + inc_x[i] for i in range(len(x1))], [y, y]

    # Add the division's lines for each column
    for i in range(8):
        ax.axhline(i, color='grey', lw=1)

    # Add the bar for each of the column based on the data received
    # TODO: Provide the data and escale between 0, 5.5
    result_column_width = column_width / 2
    initial_position = column_width + column_distance
    position = [0] + [initial_position * i for i in range(1, num_divisions)]
    for i in range(num_divisions):
        ax.bar(position[i], y, bottom=0, color="green", edgecolor='none', width=result_column_width)

    # Hide the x-axis and y-axis
    ax.axis('off')

    # Set the limits for the x-axis and y-axis
    ax.set_xlim([-1.25, (column_width + column_distance) * 4 - column_distance + column_width])
    ax.set_ylim([-0.5, num_divisions + 1])


if __name__ == '__main__':
    # create_first_figure()
    create_second_figure()

    plt.show()
