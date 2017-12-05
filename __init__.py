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

from mycroft import MycroftSkill, intent_handler
from mycroft.messagebus.message import Message
from mycroft.audio import wait_while_speaking

import time


class NapTimeSkill(MycroftSkill):
    """
        Skill to handle mycroft speech client listener sleeping and
        awakening.
    """
    def initialize(self):
        self.add_event('recognizer_loop:awoken', self.handle_awoken)

    @intent_handler(IntentBuilder("NapTimeIntent").require("SleepCommand"))
    def handle_go_to_sleep(self, message):
        """
            Intent handler for "go to sleep" command.

            Sends a message to the speech client setting the listener in a
            sleep mode.
        """
        self.emitter.emit(Message('recognizer_loop:sleep'))
        self.speak_dialog("sleep")
        time.sleep(2)
        wait_while_speaking()
        self.enclosure.eyes_narrow()

    def handle_awoken(self, message):
        """
            Handler for the recognizer_loop:awoken message (sent when the
            listener in the speech client is awoken.

            Speak the "I am awake" dialog and reset eyes to ready state.
        """
        self.enclosure.eyes_blink('b')
        self.speak_dialog("iamawake")
        time.sleep(2)
        wait_while_speaking()
        self.enclosure.eyes_reset()

    def stop(self):
        pass


def create_skill():
    return NapTimeSkill()
