from datetime import datetime
from pathlib import Path
from tempfile import gettempdir

from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from pandas import DataFrame
from pandera import SchemaModel
from pandera.typing import Series

from pandera_provider.operators.pandera import PanderaOperator

TMPDIR = gettempdir()
TMPFILE = Path(TMPDIR, "test.csv")


class InputSchema(SchemaModel):
    column1: Series[str]
    column2: Series[int]
    column3: Series[float]


def generate_dataframe():
    df = DataFrame(
        {
            "column1": ["pandera", "is", "awesome"],
            "column2": [1, 2, 3],
            "column3": [0.1, 0.2, 0.3],
        }
    )
    df.to_csv(TMPFILE, index=False)


@dag(
    dag_id="schema_model_csv_dag",
    start_date=datetime(2022, 1, 1),
    catchup=False,
    schedule="0 0 * * *",
)
def schema_model_success_dag(**kwargs):

    generate_dataframe_task = PythonOperator(
        task_id="generate_dataframe_task",
        python_callable=generate_dataframe,
    )

    validate_dataframe_task = PanderaOperator(
        filepath=TMPFILE,
        task_id="validate_dataframe_task",
        schema_model=InputSchema,
    )

    generate_dataframe_task >> validate_dataframe_task


schema_model_success_dag()
