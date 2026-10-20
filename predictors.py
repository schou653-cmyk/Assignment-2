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

    def validate_patient(self, patient):
        """
        Check that Feature1 through Feature9 fall within historical [min, max].
        Raises OutOfSampleError for the first out-of-range feature encountered.
        """
        for i in range(1, 10):
            feature = f"Feature{i}"
            if feature in patient:
                col_min = self.historical_data.get_column_min(feature)
                col_max = self.historical_data.get_column_max(feature)
                val = patient[feature]

                if val < col_min or val > col_max:
                    raise OutOfSampleError(
                        f"{feature} with value {val} is outside historical range [{col_min}, {col_max}]"
                    )


class MajorityClassPredictor(Predictor):

    def __init__(self, historical_data):
        super().__init__(historical_data)
        tumor_types = self.historical_data.get_column("TumorType")
        benign = tumor_types.count(0.0)
        malignant = tumor_types.count(1.0)
        self.majority_class = 0 if benign >= malignant else 1

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
        Calculate Euclidean distance using Feature1-Feature9 only (not TumorType).
        """
        total = 0.0
        for i in range(1, 10):
            feature = f"Feature{i}"
            diff = patient1[feature] - patient2[feature]
            total += diff ** 2
        return math.sqrt(total)

    def predict(self, patient):
        """
        Find the closest historical patient and return their TumorType.
        """
        self.validate_patient(patient)
        closest_distance = float("inf")
        prediction = None

        for historical_patient in self.historical_data.data:
            d = self.distance(patient, historical_patient)
            if d < closest_distance:
                closest_distance = d
                prediction = int(historical_patient["TumorType"])

        return prediction