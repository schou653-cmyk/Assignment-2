from data_representation import DataTable
from predictors import MajorityClassPredictor, NearestNeighborPredictor
from exceptions1 import OutOfSampleError


def calculate_accuracy(predictions, actual):
    """
    Calculate prediction accuracy percentage.
    """
    if len(predictions) != len(actual):
        raise ValueError("Predictions and labels must be same length")
    if len(actual) == 0:
        raise ValueError("Cannot calculate without any patients")

    correct = sum(1 for p, y in zip(predictions, actual) if p == y)
    return (correct / len(actual)) * 100.0


def main():
    # 1. Load datasets
    historical = DataTable("cancer_historical.csv")
    new_cases = DataTable("cancer_new_cases.csv", historical_averages=historical.column_averages)
    labels = DataTable("cancer_new_cases_labels.csv")

    # 2. Instantiate predictors
    mode_predictor = MajorityClassPredictor(historical)
    nn_predictor = NearestNeighborPredictor(historical)

    mode_predictions = []
    nn_predictions = []
    valid_labels = []

    actual_labels = labels.get_column("TumorType")

    # 3. Predict for every new case, catching out-of-sample exceptions
    for i in range(len(new_cases.data)):
        patient = new_cases.get_row(i)
        try:
            p_mode = mode_predictor.predict(patient)
            p_nn = nn_predictor.predict(patient)

            mode_predictions.append(p_mode)
            nn_predictions.append(p_nn)
            valid_labels.append(actual_labels[i])
        except OutOfSampleError as e:
            print(f"Patient {i}: {e}")

    # 4. Accuracy evaluation against valid labels
    print(f"Majority Class (Mode) accuracy:      {calculate_accuracy(mode_predictions, valid_labels):.2f}%")
    print(f"Nearest Neighbor (1-NN) accuracy:    {calculate_accuracy(nn_predictions, valid_labels):.2f}%")


if __name__ == "__main__":
    main()