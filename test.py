import pytest
import main


@pytest.fixture
def test_message():
    return Message(
        chat=Chat(id=0)  # введи вместо 0, то чему равно id
    )


def test_game_start():
    try:
        args = main.start_game(test_message)  # [arg1 = 1, arg2 = 2, ...]
        ans = (1, 2, ...)
        for i in range(len(args)):
            assert args[i] == ans[i]
    except FileNotFoundError:
        ...


@pytest.fixture
def test_user():
    return (main.start_game(message=test_message))