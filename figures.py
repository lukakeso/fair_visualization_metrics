import matplotlib.pyplot as plt
from analysis.graphics import Graphics


def example_data():
    data = {
        'Findable': {
            'labels': ['RDA-F1-01M', 'RDA-F1-01D', 'RDA-F1-02M', 'RDA-F1-02D', 'RDA-F2-01M', 'RDA-F3-01M',
                       'RDA-F4-01M'],
            'data': [1, 2, 3, 4, 1, 2, 3]
        },
        'Accessible': {
            'labels': ['RDA-A1-01M', 'RDA-A1-02M', 'RDA-A1-02D', 'RDA-A1-03M', 'RDA-A1-03D', 'RDA-A1-04M',
                       'RDA-A1-04D', 'RDA-A1-05D', 'RDA-A1.1-01M', 'RDA-A1.1-01D', 'RDA-A1.2-01D', 'RDA-A2-01M'],
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


if __name__ == '__main__':
    data = example_data()
    gph = Graphics(data=data)

    gph.create_first_figure()
    gph.create_second_figure()
    gph.pie_chart()

    plt.show()
