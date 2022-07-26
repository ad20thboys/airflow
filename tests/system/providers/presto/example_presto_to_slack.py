#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
Example DAG using PrestoToSlackOperator.
"""

import os
from datetime import datetime

from airflow import models
from airflow.providers.presto.transfers.presto_to_slack import PrestoToSlackOperator

PRESTO_TABLE = os.environ.get("PRESTO_TABLE", "test_table")
ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")
DAG_ID = "example_presto_to_slack"
SLACK_CONN_WEBHOOK = 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX'

with models.DAG(
    dag_id=DAG_ID,
    schedule_interval='@once',  # Override to match your needs
    start_date=datetime(2022, 1, 1),
    catchup=False,
    tags=["example"],
) as dag:
    # [START howto_operator_presto_to_slack]
    PrestoToSlackOperator(
        task_id="presto_to_slack",
        slack_token=SLACK_CONN_WEBHOOK,
        sql=f"SELECT col FROM {PRESTO_TABLE}",
        slack_channel="my_channel",
        slack_message="message: {{ ds }}, {{ results_df }}",
    )
    # [END howto_operator_presto_to_slack]


from tests.system.utils import get_test_run  # noqa: E402

# Needed to run the example DAG with pytest (see: tests/system/README.md#run_via_pytest)
test_run = get_test_run(dag)
