def normalize_string(text):
    return text.strip().replace(" ", "_").lower()


def get_metadata(text):
    return text.split(",")
