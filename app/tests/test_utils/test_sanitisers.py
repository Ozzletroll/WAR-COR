from app.utils.sanitisers import sanitise_input


def test_sanitise_input():

    value = '<img src="image.jpg"/>'
    expected_output = '<img src="image.jpg"/>'
    assert sanitise_input(value, allow_images=True) == expected_output

    value = '<img src="image.jpg"/>'
    expected_output = '<p>&lt;img src="image.jpg"/&gt;</p>'
    assert sanitise_input(value, allow_images=False) == expected_output

    value = '<p style="disallowed style tag">Text with disallowed style</p>'
    expected_output = '<p style="">Text with disallowed style</p>'
    print(sanitise_input(value))
    assert sanitise_input(value) == expected_output

    value = '<script>Text with disallowed tag</script>'
    expected_output = '<p>&lt;script&gt;Text with disallowed tag&lt;/script&gt;</p>'
    print(sanitise_input(value))
    assert sanitise_input(value) == expected_output

    value = "Text without tags"
    expected_output = "<p>Text without tags</p>"
    assert sanitise_input(value) == expected_output
