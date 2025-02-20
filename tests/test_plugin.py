# Licensed to Elasticsearch B.V. under one or more contributor
# license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright
# ownership. Elasticsearch B.V. licenses this file to you under
# the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import pytest

def test_generates_tests_from_list_tracks(pytester, example, temp_repo):
    expected = [
        "test_track_challenge[test-track-index-and-query]",
        "test_track_challenge[test-track-index-only]",
    ]
    generated, _ = pytester.inline_genitems(example, f"--track-repository={temp_repo}")
    assert [func.name for func in generated] == expected

def test_runs_correct_race_commands(caplog, temp_repo, run):
    def expected_log_line(track, challenge):
        command = (
            f'esrally race --track="{track}" --challenge="{challenge}" '
            f'--track-repository="{temp_repo}" --track-revision="master" '
            '--configuration-name="pytest" --enable-assertions --kill-running-processes '
            '--on-error="abort" --pipeline="benchmark-only" --target-hosts="127.0.0.1:19200" --test-mode'
        )

        return ("pytest_rally.rally", "INFO", f'Running command: [{command}]')

    challenges = [
        "index-and-query",
        "index-only",
    ]

    expected = [expected_log_line("test-track", challenge) for challenge in challenges]
    res = run()
    actual = [(r.name, r.levelname, r.message) for r in caplog.records if "esrally race" in r.message]
    assert actual == expected
