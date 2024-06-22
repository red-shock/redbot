import toml


class Preferences:
    def __init__(self, path: str) -> None:
        self.path = path
        self.data = toml.load(self.path)

    def get_delete_duplicate_messages(self) -> bool:
        return self.data["server preferences"]["delete_duplicate_messages"]

    def set_delete_duplicate_messages(self, value: bool) -> None:
        self.data["server preferences"]["delete_duplicate_messages"] = value
        with open(self.path, "w") as file:
            toml.dump(self.data, file)

    delete_duplicate_messages = property(
        get_delete_duplicate_messages, set_delete_duplicate_messages
    )


if __name__ == "__main__":
    preference = Preferences("preferences.toml")
    print(preference.delete_duplicate_messages)
