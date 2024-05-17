from app.utils.sanitisers import sanitise_input


def test_sanitise_input():

    value = '<img src="image.jpg"/>'
    expected_output = '<img src="image.jpg"/>'
    assert sanitise_input(value, allow_images=True) == expected_output

    value = '<img src="image.jpg"/>'
    expected_output = ''
    assert sanitise_input(value, allow_images=False) == expected_output

    value = '<script>Text with disallowed tag</script>'
    expected_output = ''
    assert sanitise_input(value) == expected_output

    value = "Text without tags"
    expected_output = "<p>Text without tags</p>"
    assert sanitise_input(value) == expected_output

    value = "Message body that shouldn't have p tags"
    expected_output = "Message body that shouldn't have p tags"
    assert sanitise_input(value, wrap=False) == expected_output

    value = '<a href="http://www.google.com">LINK TEXT</a>'
    expected_output = '<a href="http://www.google.com" rel="noopener noreferrer nofollow">LINK TEXT</a>'
    assert sanitise_input(value, wrap=False) == expected_output
