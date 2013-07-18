def normalize_string(text):
    return text.replace(" ", "_").lower()


def get_metadata(text):
    return text.split(",")
