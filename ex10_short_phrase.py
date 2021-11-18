class TestPhrase:
    def test_short_phrase(self):
        phrase = input("Set a phrase: ")
        check_len = 15
        assert len(phrase) < check_len, f"The length of the phrase must be less than {check_len} characters"
