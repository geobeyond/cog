# Copyright 2018 Geobeyond Srl

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

_services = {}

def get(name):
    return _services[name]

def set(name, service):
    _services[name] = service
    return service

def getNames():
    return list(_services.keys())

def getAll():
    return _services