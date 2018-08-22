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
    help = 'starts dev server without reload; use with an IDE\'s remote debugger'

    def add_arguments(self, parser):
        parser.add_argument('addrport', nargs='?', default='0.0.0.0:3000', help='Optional port number, or ipaddr:port')

    def handle(self, *args, **options):
        cmd = 'python manage.py runserver {0} --noreload'.format(options['addrport'])
        subprocess.call(cmd, shell=True)
