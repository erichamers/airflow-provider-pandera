from typing import Any, Dict

from airflow.models import BaseOperator
from pandas import DataFrame
from pandera import DataFrameSchema


class DataFrameSchemaOperator(BaseOperator):
    """
    Provides an operator for running validations in the data using the
    DataFrameSchema.

    Methods
    ------
    execute(context={})
        Executes the operator.
    """

    def __init__(
        self,
        dataframe: DataFrame,
        columns: dict,
        *args,
        **kwargs,
    ) -> None:
        """
        Parameters
        ----------
        dataframe: DataFrame
            A dataframe object
        columns: dict
            A dictionary containing the mapping between columns and types.
        """
        super().__init__(*args, **kwargs)
        self.dataframe = dataframe
        self.columns = columns
        self.__dict__.update(kwargs)

    def execute(self, context: Dict[str, Any] = {}) -> Any:
        """
        Runs the operator.

        Parameters
        ---------
        context: dict
            Context provided by Airflow.
        """
        schema = DataFrameSchema(columns=self.columns)
        results = schema.validate(self.dataframe)
        return results
