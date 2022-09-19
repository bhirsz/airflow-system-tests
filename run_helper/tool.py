# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import subprocess
import time
from datetime import datetime
from typing import Optional

import click
from rich.console import Console
from rich.live import Live
from rich.table import Table

QUERY_BUILDS_CMD = (
    "gcloud builds list "
    "--filter tags='{build_id}' "
    "--format json("
    "status,substitutions._TEST_NAME,"
    "timing.BUILD.startTime,"
    "timing.BUILD.endTime"
    ")"
)


def get_builds(cmd):
    result = subprocess.run(cmd.split(), capture_output=True)
    if result.stderr:
        raise RuntimeError(result.stderr)
    return json.loads(result.stdout)


def parse_timestamp(time_str):
    format_in = "%Y-%m-%dT%H:%M:%S.%f"
    format_out = "%Y-%m-%d %H:%M:%S"
    time_obj = datetime.strptime(time_str[:26], format_in)
    return time_obj.strftime(format_out)


def get_results_table(cmd, filter_status):
    table = Table()
    table.add_column("Test name")
    table.add_column("Status")
    table.add_column("Start time")
    table.add_column("End time")
    builds = get_builds(cmd)
    for build in builds:
        test_name = build["substitutions"]["_TEST_NAME"]
        status = build["status"]
        if filter_status is not None and status != filter_status:
            continue
        start_time = parse_timestamp(build["timing"]["BUILD"]["startTime"])
        end_time = parse_timestamp(build["timing"]["BUILD"]["endTime"])
        table.add_row(test_name, status, start_time, end_time)
    return table


@click.group(name="airflow-system")
@click.version_option(version="alpha", prog_name="airflow-system")
def cli():
    """
    Utility tool for Airflow System tests executed in the Google Cloud.
    """
    pass


@cli.command()
@click.option("--build-id", type=str, required=True)
@click.option("--keep-alive", is_flag=True, default=False)
@click.option(
    "--filter-status",
    type=click.Choice(["SUCCESS", "FAILURE"]),
    help="Filter results by test status",
)
def results(
    build_id: str, keep_alive: bool = False, filter_status: Optional[str] = None
):
    """Get system tests results from BigQuery table."""
    cmd = QUERY_BUILDS_CMD.format(build_id=build_id)
    if keep_alive:
        with Live(
            get_results_table(cmd, filter_status), auto_refresh=False
        ) as live:
            while True:
                time.sleep(5)
                live.update(get_results_table(cmd, filter_status), refresh=True)
    else:
        console = Console()
        console.print(get_results_table(cmd, filter_status))


if __name__ == "__main__":
    cli()
