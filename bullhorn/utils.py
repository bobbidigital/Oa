from bullhorn.shortcuts import categories_for_forms

def normalize_string(text):
    return text.strip().replace(" ", "_").lower()


def get_metadata(text):
    return text.split(",")


def get_tag_fields():
    categories = categories_for_forms(include_device=True)
    fields = [normalize_string(category.name)
              for category in categories]
    fields.append('contacts')
    return fields

