import matplotlib.pyplot as plt
from analysis.radar import radar_factory
import numpy as np


class Graphics:
    def __init__(self, data):
        self.data = data

    def create_first_figure(self):
        theta = {
            'Findable': radar_factory(num_vars=len(self.data['Findable']['labels']), frame='polygon'),
            'Accessible': radar_factory(num_vars=len(self.data['Accessible']['labels']), frame='polygon'),
            'Interoperable': radar_factory(num_vars=len(self.data['Interoperable']['labels']), frame='polygon'),
            'Reusable': radar_factory(num_vars=len(self.data['Reusable']['labels']), frame='polygon')
        }

        # Create the first radar chart in Figure 1
        fig, axs = plt.subplots(figsize=(9, 9), nrows=2, ncols=2, subplot_kw=dict(projection='radar'))

        fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

        zipped = [[array_element, key, value] for array_element, (key, value) in zip(axs.flat, self.data.items())]
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

    def create_second_figure(self):
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
        # TODO: need to calculate -0.1 in function of the dimensions of the case, 0.1 is = -0.1 + 0.2
        #  (extension of the line)
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
        y = [0.5, 1.5, 3.5, 5.48]
        for i in range(4):
            ax.bar(position[i], y[i], bottom=0, color="green", edgecolor='none', width=result_column_width)

        # Hide the x-axis and y-axis
        ax.axis('off')

        # Set the limits for the x-axis and y-axis
        ax.set_xlim([-1.25, (column_width + column_distance) * 4 - column_distance + column_width])
        ax.set_ylim([-0.5, num_divisions + 1])

    def pie_chart(self):
        def func(pct, allvals):
            absolute = int(np.round(pct / 100. * np.sum(allvals)))
            return f"{absolute:d}\n({pct:.1f}%)"

        # Data for the pie chart
        labels = ['Essential', 'Important', 'Useful']
        sizes = [7, 20, 14]

        # Create the figure and axes
        fig, ax = plt.subplots()

        # Generate the pie chart
        wedges, texts, autotexts = ax.pie(sizes,
                                          autopct=lambda pct: func(pct, sizes),
                                          shadow=True,
                                          startangle=90,
                                          textprops=dict(weight="bold", color="black", size="large"))

        # Add a title
        ax.set_title('Distribution of priorities')

        # legend
        ax.legend(wedges, labels,
                  loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1))

        # Add number and percentage labels
        for text, autotext in zip(texts, autotexts):
            percentage = autotext.get_text()
            value = text.get_text()
            # ax.text3D(0, 0, 1, f'{value}\n{percentage}', ha='center', va='center')
            # ax.text3D(0, 0, 1, f'{label}\n{size}\n{percentage}', ha='center', va='center')

        # Hide the x-axis and y-axis
        ax.axis('off')
