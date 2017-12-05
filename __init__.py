# Copyright 2017, Mycroft AI Inc.
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

from adapt.intent import IntentBuilder

from mycroft.messagebus.message import Message
from mycroft.skills.core import MycroftSkill
from mycroft.audio import wait_while_speaking

import time


class NapTimeSkill(MycroftSkill):
    def __init__(self):
        super(NapTimeSkill, self).__init__(name="NapTimeSkill")

    def initialize(self):
        naptime_intent = IntentBuilder("NapTimeIntent").require(
            "SleepCommand").build()
        self.register_intent(naptime_intent, self.handle_intent)

        self.add_event('recognizer_loop:awoken', self.handle_awoken)

    def handle_intent(self, message):
        self.emitter.emit(Message('recognizer_loop:sleep'))
        self.speak_dialog("sleep")
        time.sleep(2)
        wait_while_speaking()
        self.enclosure.eyes_narrow()

    def handle_awoken(self, message):
        self.enclosure.eyes_blink('b')
        self.speak_dialog("iamawake")
        time.sleep(2)
        wait_while_speaking()
        self.enclosure.eyes_reset()

    def stop(self):
        pass


def create_skill():
    return NapTimeSkill()
