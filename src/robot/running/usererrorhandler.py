#  Copyright 2008-2015 Nokia Networks
#  Copyright 2016-     Robot Framework Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from robot.model import Tags
from robot.result import Keyword as KeywordResult
from robot.variables import VariableAssignment

from .arguments import ArgumentSpec
from .statusreporter import StatusReporter


class UserErrorHandler:
    """Created if creating handlers fail. Running it raises DataError.

    The idea is not to raise DataError at processing time and prevent all
    tests in affected test case file from executing. Instead, UserErrorHandler
    is created and if it is ever run DataError is raised then.
    """
    supports_embedded_arguments = False

    def __init__(self, error, name, owner=None, source=None, lineno=None):
        """
        :param robot.errors.DataError error: Occurred error.
        :param str name: Name of the affected keyword.
        :param str owner: Name of the affected library or resource.
        :param str source: Path to the source file.
        :param int lineno: Line number of the failing keyword.
        """
        self.error = error
        self.name = name
        self.owner = owner
        self.source = source
        self.lineno = lineno
        self.arguments = ArgumentSpec()
        self.timeout = None
        self.tags = Tags()

    @property
    def full_name(self):
        return f'{self.owner}.{self.name}' if self.owner else self.name

    @property
    def doc(self):
        return f'*Creating keyword failed:* {self.error}'

    @property
    def short_doc(self):
        return self.doc.splitlines()[0]

    def create_runner(self, name, languages=None):
        return self

    def run(self, kw, context, run=True):
        result = KeywordResult(name=self.name,
                               owner=self.owner,
                               args=kw.args,
                               assign=tuple(VariableAssignment(kw.assign)),
                               type=kw.type)
        with StatusReporter(kw, result, context, run):
            if run:
                raise self.error

    dry_run = run
