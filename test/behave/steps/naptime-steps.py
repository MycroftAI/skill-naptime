
# Copyright 2020 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import time

from behave import given, when

from mycroft.messagebus import Message

@given('a device is asleep')
def sleep_device(context):
    context.bus.emit(Message('recognizer_loop:sleep'))
    time.sleep(2)

@when('a wake up message is emitted')
def emit_wake_up(context):
    context.bus.emit(Message('mycroft.awoken'))
