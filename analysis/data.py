from json import load
from os.path import dirname, join
import re


class Data(object):
    def __init__(self):
        root_path = dirname(dirname(__file__))
        filename = join(root_path, 'data', 'example.json')

        with open(file=filename, mode='r') as f:
            self.raw_data = load(f)

        self.pattern = re.compile(r"RDA-([FAIR]).+-.*", flags=0)

        self.fair_maturity_model_data = dict()
        self.FMMClassification_data = dict()
        self.FMMClassification_data_length = int()
        self.fairness_classification_per_indicator = dict()

        self.get_fair_maturity_model()
        self.get_fdm_classification()
        self.get_fairness_classification_per_indicator()

    def get_fair_maturity_model(self) -> None:
        fair_maturity_model = {
            'FDMFE1[SQ001]': 'RDA-F1-01M',
            'FDMFE1[SQ002]': 'RDA-F1-01D',
            'FDMFE1[SQ003]': 'RDA-F1-02M',
            'FDMFE1[SQ004]': 'RDA-F1-02D',
            'FDMFE1[SQ005]': 'RDA-F2-01M',
            'FDMFE1[SQ006]': 'RDA-F3-01M',
            'FDMFE1[SQ007]': 'RDA-F4-01M',
            'FDMAE1[SQ001]': 'RDA-A1-02M',
            'FDMAE1[SQ002]': 'RDA-A1-02D',
            'FDMAE1[SQ003]': 'RDA-A1-03M',
            'FDMAE1[SQ004]': 'RDA-A1-03D',
            'FDMAE1[SQ005]': 'RDA-A1-04M',
            'FDMAE1[SQ006]': 'RDA-A1-04D',
            'FDMAE1[SQ007]': 'RDA-A1.1-01M',
            'FDMAE1[SQ008]': 'RDA-A2-01M',
            'FDMAI1[SQ001]': 'RDA-A1-01M',
            'FDMAI1[SQ002]': 'RDA-A1.1-01D',
            'FDMAI1[SQ003]': 'RDA-A1-05D',
            'FDMAU1[SQ001]': 'RDA-A1.2-01D',
            'FDMRE1[SQ001]': 'RDA-R1-01M',
            'FDMRE1[SQ002]': 'RDA-R1.1-01M',
            'FDMRE1[SQ003]': 'RDA-R1.3-01M',
            'FDMRE1[SQ004]': 'RDA-R1.3-01D',
            'FDMRE1[SQ005]': 'RDA-R1.3-02M',
            'FDMRI1[SQ001]': 'RDA-R1.1-02M',
            'FDMRI1[SQ002]': 'RDA-R1.1-03M',
            'FDMRI1[SQ003]': 'RDA-R1.2-01M',
            'FDMRI1[SQ004]': 'RDA-R1.3-02D',
            'FDMRU1[SQ001]': 'RDA-R1.2-02M',
            'FDMII1[SQ001]': 'RDA-I1-01M',
            'FDMII1[SQ002]': 'RDA-I1-01D',
            'FDMII1[SQ003]': 'RDA-I1-02M',
            'FDMII1[SQ004]': 'RDA-I1-02D',
            'FDMII1[SQ005]': 'RDA-I2-01M',
            'FDMII1[SQ006]': 'RDA-I3-01M',
            'FDMII1[SQ007]': 'RDA-I3-03M',
            'FDMIU1[SQ001]': 'RDA-I2-01D',
            'FDMIU1[SQ002]': 'RDA-I3-01D',
            'FDMIU1[SQ003]': 'RDA-I3-02M',
            'FDMIU1[SQ004]': 'RDA-I3-02D',
            'FDMIU1[SQ005]': 'RDA-I3-04M'
        }

        self.fair_maturity_model_data = {fair_maturity_model[key]: int(self.raw_data['responses'][0][key])
                                         for key in fair_maturity_model.keys()}

    def get_fdm_classification(self) -> None:
        fmm_classification = {
            'Essential': [
                'RDA-F1-01M', 'RDA-F1-01D', 'RDA-F1-02M', 'RDA-F1-02D', 'RDA-F2-01M', 'RDA-F3-01M', 'RDA-F4-01M',
                'RDA-A1-02M', 'RDA-A1-02D', 'RDA-A1-03M', 'RDA-A1-03D', 'RDA-A1-04M', 'RDA-A1-04D', 'RDA-A1.1-01M',
                'RDA-A2-01M', 'RDA-R1-01M', 'RDA-R1.1-01M', 'RDA-R1.3-01M', 'RDA-R1.3-01D', 'RDA-R1.3-02M'
            ],
            'Important': [
                'RDA-A1-01M', 'RDA-A1-05D', 'RDA-A1.1-01D', 'RDA-I1-01M', 'RDA-I1-01D', 'RDA-I1-02M', 'RDA-I1-02D',
                'RDA-I2-01M', 'RDA-I3-01M', 'RDA-I3-03M', 'RDA-R1.1-02M', 'RDA-R1.1-03M', 'RDA-R1.2-01M',
                'RDA-R1.3-02D'
            ],
            'Useful': [
                'RDA-A1.2-01D', 'RDA-I2-01D', 'RDA-I3-01D', 'RDA-I3-02M', 'RDA-I3-02D', 'RDA-I3-04M', 'RDA-R1.2-02M'
            ]
        }

        self.FMMClassification_data = {
            'Essential': self.__classification_per_category__(classes=fmm_classification, category='Essential'),
            'Important': self.__classification_per_category__(classes=fmm_classification, category='Important'),
            'Useful': self.__classification_per_category__(classes=fmm_classification, category='Useful')
        }

        self.FMMClassification_data_length = {
            'Essential': self.__len_classification_per_category__(category='Essential'),
            'Important': self.__len_classification_per_category__(category='Important'),
            'Useful': self.__len_classification_per_category__(category='Useful')
        }

    def get_fairness_classification_per_indicator(self):
        self.fairness_classification_per_indicator = self.__classification_per_indicator__()

    def __classification_per_category__(self, classes: dict, category: str) -> dict:
        result = {
            'F': 'Findable',
            'A': 'Accessible',
            'I': 'Interoperable',
            'R': 'Reusable'
        }

        # Create the structure
        aux1 = {x: dict() for x in [result[x] for x in result]}
        aux2 = {key: self.fair_maturity_model_data[key] for key in classes[category]}

        for key, value in aux2.items():
            category = self.pattern.findall(key)

            if category is None:
                raise Exception(f"Sorry, key is not expected: {key}")

            aux1[result[category[0]]][key] = value

        return aux1

    def __len_classification_per_category__(self, category: str) -> int:
        value = sum([len(self.FMMClassification_data[category][x]) for x in self.FMMClassification_data[category]])
        return value

    def __classification_per_indicator__(self) -> dict:
        result = {
            'F': 'Findable',
            'A': 'Accessible',
            'I': 'Interoperable',
            'R': 'Reusable'
        }

        final_data = {
            'Findable': dict(),
            'Accessible': dict(),
            'Interoperable': dict(),
            'Reusable': dict()

        }

        for key, value in self.fair_maturity_model_data.items():
            aux = result[self.pattern.findall(key)[0]]

            if aux is None:
                raise Exception(f"Sorry, key is not expected: {key}")

            final_data[aux][key] = value

        return final_data


if __name__ == '__main__':
    d = Data()
    print(d.FMMClassification_data)
