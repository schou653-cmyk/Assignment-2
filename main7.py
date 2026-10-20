from data_representation import DataTable
from predictors import MajorityClassPredictor, NearestNeighborPredictor
from exceptions1 import OutOfSampleError


def calculate_accuracy(predictions, actual):
    """
    Calculate prediction accuracy.
    """

    if len(predictions) != len(actual):
        raise ValueError (" Predictions and labels must be same length")

    if len(actual) == 0:
        raise ValueError(" Cannot calculate without any patients")

    correct = 0

    for prediction, diagnosis in zip(predictions, actual):
        if prediction == diagnosis:
            correct += 1

    return (correct /len(actual)) * 100


def main():

    # Load datasets
    historical = DataTable("cancer_historical1.csv")
    new_cases = DataTable("cancer_new_cases1.csv", historical.column_averages)
    labels = DataTable("cancer_new_cases_labels1.csv")


    # Create predictors
    mode_predictor = MajorityClassPredictor(historical)
    nn_predictor = NearestNeighborPredictor(historical)


    mode_predictions = []
    nn_predictions = []
    valid_labels = []

    actual_labels = labels.get_column("TumorType")


    # Predict every new case
    for i in range(len(new_cases.data)):

        patient = new_cases.get_row(i)

        try:
            mode_predictions.append(
                mode_predictor.predict(patient)
            )

            nn_predictions.append(
                nn_predictor.predict(patient)
            )

            valid_labels.append(actual_labels[i])


        except OutOfSampleError as e:
            print(f"Patient {i}: {e}")



    # Accuracy
    print(
        "Mode accuracy:",
        calculate_accuracy(mode_predictions, actual_labels),
    "%"
    )

    print(
        "Nearest Neighbor accuracy:",
        calculate_accuracy(nn_predictions, actual_labels),
   "%"
   )


if __name__ == "__main__":
    main()