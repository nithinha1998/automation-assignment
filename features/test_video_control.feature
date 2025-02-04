Feature: Indee test automation
  Scenario: user login to indee and change video settings and controls
    Given the user is signed in and navigated to project
    When the user pauses and resumes video, adjusts volume to 50% and changes resolution from 480p to 720p
    Then the video should play at 720p with 50% volume
