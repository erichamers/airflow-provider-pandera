from datetime import datetime

from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from pandas import DataFrame
from pandera import SchemaModel
from pandera.typing import Series

from pandera_provider.operators import PanderaOperator


class InputSchema(SchemaModel):
    column1: Series[int]


def generate_dataframe(**kwargs):
    ti = kwargs["ti"]
    df = DataFrame({"column1": ["pandera", "is", "awesome"]})
    ti.xcom_push("dfs_operator_df", df)


@dag(
    dag_id="schema_model_fail_dag",
    start_date=datetime(2022, 1, 1),
    catchup=False,
    schedule="0 0 * * *",
)
def schema_model_fail_dag(**kwargs):

    generate_dataframe_task = PythonOperator(
        task_id="generate_dataframe_task",
        python_callable=generate_dataframe,
    )

    validate_dataframe_task = PanderaOperator(
        task_id="validate_dataframe_task",
        schema_model=InputSchema,
    )

    generate_dataframe_task >> validate_dataframe_task


schema_model_fail_dag()
