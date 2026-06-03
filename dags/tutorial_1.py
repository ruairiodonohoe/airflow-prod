import textwrap
from datetime import datetime, timedelta

from airflow.sdk import dag, task

default_args = {
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    "tutorial",
    default_args=default_args,
    description="A simple tutorial DAG",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["example"],
)
def tutorial_dag():
    """
    This is a documentation placed anywhere
    """

    @task.bash
    def print_date():
        """
        #### Task Documentation
        You can document your task using the attributes `doc_md` (markdown),
        `doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
        rendered in the UI's Task Instance Details page.
        ![img](https://imgs.xkcd.com/comics/fixing_problems.png)
        **Image Credit:** Randall Munroe, [XKCD](https://xkcd.com/license.html)
        """
        return "date"

    @task.bash(depends_on_past=False, retries=3)
    def sleep_task():
        return "sleep 5"

    templated_command = textwrap.dedent("""
        {% for i in range(5) %}
            echo "{{ ds }}"
            echo "{{ macros.ds_add(ds, 7)}}"
        {% endfor %}
        """)

    @task.bash(depends_on_past=False)
    def templated():
        return templated_command

    print_date() >> [sleep_task(), templated()]


tutorial_dag()
