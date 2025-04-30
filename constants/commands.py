from enum import StrEnum, unique


@unique
class CommandText(StrEnum):
    MENU = "menu"
    START = "start"
    SEARCH_POSTS = "search_posts"
    INFO = "info"
    STATISTICS = "stats"
    ADD_POST = "add_post"
    MY_POSTS = "my_posts"
    HELP = "help"
    PROFILE = "profile"
    NEWSLETTER = "newsletter"

    @classmethod
    def get_all_commands(cls):
        return ["/" + str(command.value) for command in cls]

