from abc import ABC, abstractmethod
import math

from exceptions1 import OutOfSampleError


class Predictor(ABC):

    def __init__(self, historical_data):
        """
        Store historical DataTable.
        """
        self.historical_data = historical_data

    @abstractmethod
    def predict(self, patient):
        """
        Make a prediction for one patient.
        """
        pass


    def validate_patient(self,patient):
        for i in range(1,10):
            feature = f"Feature{i}"

            minimun = self.historical_data.get_column_min(feature)
            maximum = self.historical_data.get_column_max(feature)

            if feature in patient:
                value = patient[feature]

                if value < minimun or value > maximum:
                    raise OutOfSampleError (f"{feature} is outside of historical range")
                


class MajorityClassPredictor(Predictor):

    def __init__(self, historical_data):
        super().__init__(historical_data)
        self.majority_class = None

        tumor_type = self.historical_data.get_column("TumorType")

        benign = tumor_type.count(0)
        malignant = tumor_type.count(1)

        if benign > malignant:
            self.majority_class = 0
        else:
            self.majority_class = 1

        # TODO: calculate most common TumorType

    def predict(self, patient):
        """
        Always return the most common historical TumorType.
        """
        self.validate_patient(patient)
        return self.majority_class



class NearestNeighborPredictor(Predictor):

    def __init__(self, historical_data):
        super().__init__(historical_data)

    def distance(self, patient1, patient2):
        """
        Calculate Euclidean distance using Feature1-Feature9 only.
        """

        total = 0

        for i in range(1, 10):
            feature = f"Feature{i}"

            difference = (patient1[feature] - patient2[feature]) ** 2

            total += difference

        return math.sqrt(total)




    def predict(self, patient):
        """
        Find closest historical patient and return its TumorType.
        """
        self.validate_patient(patient)
        closest_distance = float("inf")
        prediction = None

        for historical_patient in self.historical_data.data:
            distance = self.distance(patient, historical_patient)

            if distance < closest_distance:
                closest_distance = distance
                prediction = historical_patient["TumorType"]


        return prediction
    
        