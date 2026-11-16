def process_name(name):
    if not isinstance(name, str):
        return ""
    return name.strip().title()


def process_age(age):
    if isinstance(age, bool):
        return None
    try:
        return int(age)
    except (ValueError, TypeError, OverflowError):
        return None


def process_tags(tags):
    if not isinstance(tags, list):
        return []
    return [
        tag.strip().lower()
        for tag in tags
        if isinstance(tag, str)
    ]


if __name__ == "__main__":
    print("Name:", process_name("  manapriya  "))
    print("Age:", process_age("21"))
    print("Tags:", process_tags([" Python ", "FUZZING"]))
