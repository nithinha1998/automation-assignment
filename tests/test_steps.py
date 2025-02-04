from pytest_bdd import scenarios, given, when, then

scenarios('../features/test_video_control.feature')


@given("the user is signed in and navigated to project")
def user_login(page):
    page.sign_in()
    assert 'projects' in page.driver.current_url
    page.title_page()
    assert 'video' in page.driver.current_url

@when("the user pauses and resumes video, adjusts volume to 50% and changes resolution from 480p to 720p")
def user_video_setting(page):
    global volume_level, final_quality, current_quality
    volume_level, final_quality, current_quality = page.control_video()
    assert current_quality == '480p', "Video resolution should be set to 480p."

@then("the video should play at 720p with 50% volume")
def verify_video_settings():
    assert volume_level == 50, "Volume should be set to 50%."
    assert final_quality == '720p', "Video resolution should be set to 720p."

