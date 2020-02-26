Feature: mycroft-naptime

    Scenario: goto sleep
    Given an english speaking user
      When the user says "go to sleep"
      Then mycroft should send the message "recognizer_loop:sleep"
