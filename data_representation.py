import csv


class DataTable:
    def __init__(self, csv_path: str, historical_averages = None):

        self.data = []

        with open(csv_path, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                for col in row:
                    if row[col] != "?":
                        row[col] == float(row[col])
                    

                self.data.append(row)

        if historical_averages is None:

            self.column_averages = {}

            for col in self.data[0]:
                valid_values = []

                for row in self.data:
                    if row[col] != "?":
                        valid_values.append(row[col])

                average = sum(valid_values) / len(valid_values)
                self.column_averages[col] = average

        else:
            self.column_averages = historical_averages


        for row in self.data:
            for col in row:
                if row[col] == "?":
                    row[col] = self.column_averages[col]



        """
        Load CSV data into memory.
        Convert all values to float.
        """
        pass

    def get(self, row_idx: int, col_name: str):

        return self.data[row_idx][col_name]
    
        """
        Return a single value from a row and column.
        """

    def get_column(self, col_name: str) -> list:

        values = []

        for row in self.data:
            values.append(row[col_name])

        return values
        
        """
        Return all values in a column.
        """

    def get_row(self, row_idx: int) -> dict:
        """
        Return a row as {column_name: value}
        """

        return self.data[row_idx]


    def get_column_names(self) -> list:
        """
        Return list of column names.
        """

        return list(self.data[0].keys())

    def get_column_average(self, col_name: str) -> float:
        """
        Return average of a column.
        """

        values = self.get_column(col_name)

        return sum(values)/len(values)




    def get_column_min(self, col_name: str) -> float:
        """
        Return minimum value of a column.
        """

        values = self.get_column(col_name)
        return min(values)

    def get_column_max(self, col_name: str) -> float:
        """
        Return maximum value of a column.
        """
        values = self.get_column(col_name)
        return max(values)