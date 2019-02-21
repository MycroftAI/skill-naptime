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
from mycroft.configuration.config import Configuration

import time


class NapTimeSkill(MycroftSkill):
    """
        Skill to handle mycroft speech client listener sleeping and
        awakening.
    """
    def initialize(self):
        self.started_by_skill = False
        self.sleeping = False
        self.old_brightness = 30
        self.add_event('mycroft.awoken', self.handle_awoken)
        self.wake_word = Configuration.get()['listener']['wake_word']

    @intent_handler(IntentBuilder("NapTimeIntent").require("SleepCommand"))
    def handle_go_to_sleep(self, message):
        """
            Sends a message to the speech client setting the listener in a
            sleep mode.

            If the user has been told about the waking up process five times
            already, it sends a shorter message.
        """
        count = self.settings.get('Wake up count', 0)
        count += 1
        self.settings['Wake up count'] = count
        
        if count <= 5:
            self.speak_dialog('going.to.sleep', {'wake_word': self.wake_word})
        else:
            self.speak_dialog('going.to.sleep.short')
        
        self.bus.emit(Message('recognizer_loop:sleep'))
        self.sleeping = True
        self.started_by_skill = True
        wait_while_speaking()
        time.sleep(2)
        wait_while_speaking()

        # Dim and look downward to 'go to sleep'
        # TODO: Get current brightness from somewhere
        self.old_brightness = 30
        for i in range (0, (self.old_brightness - 10) // 2):
            self.enclosure.eyes_brightness(self.old_brightness - i * 2)
            time.sleep(0.15)
        self.enclosure.eyes_look("d")
        if self.config_core.get("enclosure").get("platform", "unknown") != "unknown":
            self.bus.emit(Message('mycroft.volume.mute',
                                      data={"speak_message": False}))

    def handle_awoken(self, message):
        """
            Handler for the mycroft.awoken message (sent when the listener
            hears 'Hey Mycroft, Wake Up')
        """
        started_by_skill = self.started_by_skill

        self.awaken()
        if started_by_skill:
            self.wake_up_animation()
            # Announce that the unit is awake
            self.speak_dialog("i.am.awake")
            wait_while_speaking()

    def wake_up_animation(self):
        """
            Mild animation to come out of sleep from voice command.
            Pop open eyes and wait a sec.
        """
        self.enclosure.eyes_reset()
        time.sleep(1)
        self.enclosure.eyes_blink('b')
        time.sleep(1)
        # brighten the rest of the way
        self.enclosure.eyes_brightness(self.old_brightness)

    def awaken(self):
        if self.config_core.get("enclosure").get("platform", "unknown") != "unknown":
            self.bus.emit(Message('mycroft.volume.unmute',
                                  data={"speak_message": False}))
        self.sleeping = False
        self.started_by_skill = False


def create_skill():
    return NapTimeSkill()
