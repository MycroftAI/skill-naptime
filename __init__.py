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

import time

from mycroft import AdaptIntent, MycroftSkill, intent_handler
from mycroft.audio import wait_while_speaking
from mycroft.configuration.config import Configuration
from mycroft.messagebus.message import Message


class NapTimeSkill(MycroftSkill):
    """Skill to handle mycroft speech client listener sleeping."""

    def __init__(self) -> None:
        """Initialize NapTimeSkill"""
        super().__init__()
        self.started_by_skill = False
        self.sleeping = False
        self.old_brightness = 30
        self.disabled_confirm_listening = False

    def initialize(self) -> None:
        """Perform final initialization once Skill class has loaded."""
        self.add_event('mycroft.awoken', self.handle_awoken)
        self.platform = self.config_core.get(
            "enclosure").get("platform", "unknown")
        self.wake_word = Configuration.get()['listener']['wake_word']

    @intent_handler(AdaptIntent("NapTimeIntent").require("SleepCommand"))
    def handle_go_to_sleep(self, _) -> None:
        """Sends a message to the speech client putting the listener to sleep.

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
        self.perform_sleep()

    def handle_awoken(self, _) -> None:
        """Handler for the mycroft.awoken message

        The message is sent when the listener hears 'Hey Mycroft, Wake Up',
        this handles the user interaction upon wake up.
        """
        started_by_skill = self.started_by_skill

        self.perform_awaken()
        if started_by_skill:
            # Announce that the unit is awake
            self.speak_dialog("i.am.awake")
            self.display_waking_face()

    def display_sleep_face(self) -> None:
        """Display the sleeping face depending on the platform."""
        if self.gui.connected:
            self.gui.show_page("resting.qml", override_idle=True)
        elif self.platform == "mycroft_mark_1":
            self.display_sleep_animation()

    def display_sleep_animation(self) -> None:
        """Dim and look downward to 'go to sleep'."""
        # TODO: Get current brightness from somewhere
        self.old_brightness = 30
        for i in range(0, (self.old_brightness - 10) // 2):
            self.enclosure.eyes_brightness(self.old_brightness - i * 2)
            time.sleep(0.15)
        self.enclosure.eyes_look("d")

    def display_waking_face(self) -> None:
        """Display the waking face depending on the platform."""
        if self.gui.connected:
            self.gui.remove_page("resting.qml")
            self.gui.show_page("awake.qml", override_idle=5)
            # TODO this shouldn't be necessary - remove 2 lines when fixed.
            time.sleep(5)
            self.gui.release()
        elif self.platform == 'mycroft_mark_1':
            self.display_wake_up_animation()

    def display_wake_up_animation(self) -> None:
        """Mild animation to come out of sleep from voice command.

        Pop open eyes and wait a sec.
        """
        self.enclosure.eyes_reset()
        time.sleep(1)
        self.enclosure.eyes_blink('b')
        time.sleep(1)
        # brighten the rest of the way
        self.enclosure.eyes_brightness(self.old_brightness)

    def perform_awaken(self) -> None:
        """Perform actions to wake system up."""
        if self.platform != "unknown":
            self.bus.emit(Message('mycroft.volume.unmute',
                                  data={"speak_message": False}))
        elif self.disabled_confirm_listening:
            self.enable_confirm_listening()

        self.sleeping = False
        self.started_by_skill = False

    def perform_sleep(self) -> None:
        """Perform actions to put system to sleep."""
        self.bus.emit(Message('recognizer_loop:sleep'))
        self.sleeping = True
        self.started_by_skill = True
        # TODO - Work out why this is here...
        wait_while_speaking()
        time.sleep(2)
        wait_while_speaking()
        self.display_sleep_face()
        if self.platform != "unknown":
            self.bus.emit(Message('mycroft.volume.mute',
                                  data={"speak_message": False}))
        elif self.config_core['confirm_listening']:
            self.disable_confirm_listening()

    def disable_confirm_listening(self) -> None:
        """Patch active mycroft configuration to disable listening beep."""
        msg = Message('configuration.patch',
                      data={'config': {'confirm_listening': False}}
                      )
        self.bus.emit(msg)
        self.disabled_confirm_listening = True
        self.log.info('Disabled listening chirp')

    def enable_confirm_listening(self) -> None:
        """Patch active mycroft configuration to enable listening beep."""
        msg = Message('configuration.patch',
                      data={'config': {'confirm_listening': True}}
                      )
        self.bus.emit(msg)
        self.disabled_confirm_listening = False
        self.log.info('Enabled listening chirp again')


def create_skill():
    return NapTimeSkill()
