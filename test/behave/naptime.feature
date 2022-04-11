Feature: mycroft-naptime

    Scenario: Put a device to sleep
    Given an english speaking user
      When the user says "go to sleep"
      Then mycroft should send the message "recognizer_loop:sleep"

    Scenario: Wake up a device that had been put to sleep
    Given a device is asleep
      When a wake up message is emitted
      Then "mycroft-naptime" should reply with dialog from "i.am.awake"

    Scenario: Try to wake up device that is not asleep
    Given an english speaking user
      When the user says "wake up"
      Then "mycroft-naptime" should reply with dialog from "already.awake"
