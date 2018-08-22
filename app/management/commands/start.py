# Copyright 2018 Geobeyond Srl
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'runs server with gunicorn in a production setting'

    def add_arguments(self, parser):
        parser.add_argument('addrport', nargs='?', default='0.0.0.0:3000', help='Optional ipaddr:port')

    def handle(self, *args, **options):
        cmd = 'gunicorn -b {0} cog.wsgi'.format(options['addrport'])
        subprocess.call(cmd, shell=True)