# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.


from adapt.intent import IntentBuilder

from mycroft.messagebus.message import Message
from mycroft.skills.core import MycroftSkill
from mycroft.audio import wait_while_speaking

import time
__author__ = 'seanfitz'


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
