Feature: mycroft-naptime

    Scenario: goto sleep
    Given an english speaking user
      When the user says "go to sleep"
      Then mycroft should send the message "recognizer_loop:sleep"

    Scenario: wake up
    Given a device is asleep
      When a wake up message is emitted
      Then "mycroft-naptime" should reply with dialog from "i.am.awake"
