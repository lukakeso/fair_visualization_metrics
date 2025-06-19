import matplotlib.pyplot as plt
from analysis.radar import radar_factory
import numpy as np
from typing import Optional
from .data import Data

class Graphics:
    def __init__(self, data: Data, 
                       data2: Optional[Data] = None,
                       data_name: Optional[str] = None,
                       data_name2: Optional[str] = None,
                       ):
        """
        Initializes the Graphics class for visualizing one or two datasets, 
        with optional naming for comparison purposes.

        Parameters:
        - data (Data): The primary dataset to be visualized.
        - data2 (Optional[Data]): A second dataset for comparison, if provided.
        - data_name (Optional[str]): A custom name for the primary dataset (used in legends/titles). 
                                    Defaults to the dataset's response_id.
        - data_name2 (Optional[str]): A custom name for the second dataset, if provided. 
                                    Defaults to the second dataset's response_id.
        
        Attributes:
        - self.data: Stores the primary dataset.
        - self.data2: Stores the second dataset for comparison (if provided).
        - self.overlay_plots: Boolean flag indicating if comparison plots should be generated.
        - self.data_name: Label name for the primary dataset.
        - self.data2_name: Label name for the second dataset.
        - self.cmap: A colormap from white to blue (Blues) for visual consistency in plots.
        """
        
        # primary data
        self.data = data
        
        # data for comparison
        self.data2 = data2
        
        # defining a flag to be used in functions later
        self.overlay_plots = data2 is not None
        
        # defining names for consistency between  different graphs
        # e.g. one name for one data source
        self.data_name = self.data.response_id if data_name is None else data_name
        self.data2_name = self.data2.response_id if data_name2 is None else data_name2
        
        # defining colors for consistency between graphs 
        # e.g. one color for one data source
        if self.overlay_plots:
            self.color1 = "brown"
            self.color2 = "orange"
        else:
            self.color1 = "black"

        # Create the color map from white to blue
        self.cmap = plt.cm.get_cmap('Blues')

    def create_first_figure(self, category: str):
        theta = radar_factory(num_vars=len(self.data.fairness_classification_per_indicator[category]),
                              frame='polygon')
        
        # Get the lists with the data
        labels = list(self.data.fairness_classification_per_indicator[category].keys())
        case_data = list(self.data.fairness_classification_per_indicator[category].values())

        # Create the first radar chart in Figure 1
        fig, ax = plt.subplots(figsize=(10, 12), subplot_kw=dict(projection='radar'))

        ax.set_title(label=f"{category}"+(f" {self.data_name} vs {self.data2_name}" if self.overlay_plots else ""),
                     size='large',
                     horizontalalignment='center',
                     verticalalignment='top',
                     pad=80,
                     fontsize=16,
                     color=self.cmap(1.0), 
                     weight='semibold')

        ax.plot(theta, case_data, color=self.color1, label=self.data_name if self.overlay_plots else None)
        ax.fill(theta, case_data, color=self.color1, alpha=0.25)
        
        
        if self.overlay_plots:
            case_data_2 = list(self.data2.fairness_classification_per_indicator[category].values())
            ax.plot(theta, case_data_2, color=self.color2, label=self.data2_name if self.overlay_plots else None)
            ax.fill(theta, case_data_2, color=self.color2, alpha=0.25)
        
        ax.xaxis.set_tick_params(pad=25, rotation=10)
        ax.set_varlabels(labels)

        # Add legend
        if self.overlay_plots:
            ax.legend(
                loc="center right",
                bbox_to_anchor=(1, 0, 0.5, 1.3),
                fontsize=12)
            #ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))


    def create_second_figure(self):
        # Set the number of divisions in each column
        num_divisions = 6

        # Create the figure and axes
        fig, ax = plt.subplots(figsize=(13, 8))

        # Set the width of each column
        column_width = 0.6

        # Set the distance between the columns
        column_distance = 0.8

        # Color Value based on the number of divisions
        color_value = 0.0

        # Iterate over each column
        for i in range(4):
            # Calculate the x-coordinate of the column
            x = i * (column_width + column_distance)

            # Iterate over each division within the column
            for j in range(num_divisions):
                # Calculate the color value for the division
                color_value = j / (num_divisions - 1)

                # Get the color for the division using the color map
                color = self.cmap(color_value)

                # Plot the bar for the division
                ax.bar(x, 1, bottom=j, color=color, edgecolor='none', width=column_width)

        # Add white lines at the top of each division within the column
        y = (num_divisions - 1) + 0.5 - 0.02  # the lines have linewidth=3, so to center the line we need to rest 0.01
        # TODO: need to calculate -0.1 in function of the dimensions of the case, 0.1 is = -0.1 + 0.2
        #  (extension of the line)
        x1, y1 = [-0.07, 0.07], [y, y]
        inc_x = [column_width+column_distance, column_width+column_distance]
        for i in range(num_divisions):
            plt.plot(x1, y1, color="white", linewidth=4)
            x1, y1 = [x1[i] + inc_x[i] for i in range(len(x1))], [y, y]

        # Add the division's lines for each column
        for i in range(7):
            ax.axhline(i, color='grey', lw=1)

        # Add the bar for each of the column based on the data received
        # TODO: Provide the data and escale between 0, 5.5
        result_column_width = column_width / 2
        bar_spacing = result_column_width / 2 
        initial_position = column_width + column_distance
        position = [0] + [initial_position * i for i in range(1, num_divisions)]

        y = list()
        temp_y = self.data.FMMClassification_data_compliance_level
        for i in ['Findable', 'Accessible', 'Interoperable', 'Reusable']:
            # The bar char start with min=0.5 and max=5.5, so we need to add 0.5 to the values
            y.append(temp_y[i]+0.5)
        
        if self.overlay_plots:
            y2 = list()
            temp_y2 = self.data2.FMMClassification_data_compliance_level
            for i in ['Findable', 'Accessible', 'Interoperable', 'Reusable']:
            # The bar char start with min=0.5 and max=5.5, so we need to add 0.5 to the values
                y2.append(temp_y2[i]+0.5)

        # y = [0.5, 1.5, 3.5, 0.48]
        for i in range(4):
            if self.overlay_plots:
                if i == 0:
                    ax.bar(position[i]-bar_spacing, y2[i], bottom=0, alpha=0.6, color=self.color1, edgecolor='none', width=result_column_width, label=self.data_name)
                    ax.bar(position[i]+bar_spacing, y[i], bottom=0, alpha=0.6, color=self.color2, edgecolor='none', width=result_column_width, label=self.data2_name)
                else:
                    ax.bar(position[i]-bar_spacing, y2[i], bottom=0, alpha=0.6, color=self.color1, edgecolor='none', width=result_column_width)
                    ax.bar(position[i]+bar_spacing, y[i], bottom=0, alpha=0.6, color=self.color2, edgecolor='none', width=result_column_width)
            else:
                ax.bar(position[i], y[i], bottom=0, alpha=0.6, color=self.color1, edgecolor='none', width=result_column_width)
            col_name = list({j for j in temp_y if temp_y[j] + 0.5 == y[i]})[0]
            ax.text(x=position[i], y=-0.5, s=col_name, horizontalalignment='center', fontsize=18,
                    color=self.cmap(color_value), weight='semibold')
            
            

        # Hide the x-axis and y-axis
        ax.axis('off')

        # Set the limits for the x-axis and y-axis
        ax.set_xlim([-1.25, (column_width + column_distance) * 4 - column_distance + column_width])
        ax.set_ylim([-0.5, num_divisions + 1])

        ax.set_title(label='FDM FAIRness Level score'+(f"\n{self.data_name} vs {self.data2_name}" if self.overlay_plots else ""), fontsize=24, color=self.cmap(1.0), weight='semibold')
        
        if self.overlay_plots:
            ax.legend(loc="center right",
                    bbox_to_anchor=(0.62, 0.15, 0.5, 0.5),
                    fontsize=20)

        
        
    def pie_chart(self, data, data_name="", text_color="black"):
        def func(pct, allvals):
            absolute = int(np.round(pct / 100. * np.sum(allvals)))
            return f"{absolute:d}\n({pct:.1f}%)"

        # Data for the pie chart
        labels = list(data.FMMClassification_data_length.keys())
        sizes = [data.FMMClassification_data_length[x] for x in labels]

        # Create the figure and axes
        fig, ax = plt.subplots(figsize=(15, 10))

        # Define colors for the wedges
        colors = [self.cmap(i / max(len(labels), 1)) for i in range(len(labels)+1)][-3:][::-1]
        
        # Generate the pie chart
        wedges, texts, autotexts = ax.pie(sizes,
                                          colors=colors,
                                          autopct=lambda pct: func(pct, sizes),
                                          startangle=90,
                                          textprops=dict(weight="bold", color=text_color, size=20))

        # Add a title
        ax.set_title(label=f'Distribution of priorities'+(f"\n for {data_name}" if self.overlay_plots else ""), fontsize=24, color=self.cmap(1.0), weight='semibold')

        # legend
        ax.legend(wedges, labels,
                  loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1),
                  fontsize=20,)

        # Hide the x-axis and y-axis
        ax.axis('off')        
