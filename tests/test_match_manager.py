import itertools

import pytest

from game_engine.models import MatchStatus
from server.exceptions import (
    AppError,
    MatchAlreadyStartedError,
    MatchFinishedError,
    MatchFullError,
    MatchNotFoundError,
)
from server.match_manager import (
    CODE_ALPHABET,
    CODE_LENGTH,
    DEFAULT_WORD_COUNT,
    MAX_PLAYERS,
    JoinResult,
    MatchManager,
)
from server.schemas import CreateMatchRequest, JoinMatchRequest

# 50 distinct fake 5-letter answers, enough for the largest allowed word count.
ANSWER_WORDS = [
    "".join(letters)
    for letters in itertools.islice(itertools.product("ABCDEFGHIJ", repeat=5), 50)
]


@pytest.fixture
def manager():
    return MatchManager(answer_words=ANSWER_WORDS)


def create(manager, name="Izzy", **settings) -> JoinResult:
    return manager.create_match(CreateMatchRequest(name=name, **settings))


def join(manager, code, name="Sam") -> JoinResult:
    return manager.join_match(code, JoinMatchRequest(name=name))


def test_create_match_returns_waiting_status_and_ids(manager):
    result = create(manager)

    assert isinstance(result, JoinResult)
    assert result.status == MatchStatus.WAITING
    assert result.match_id
    assert result.player_id


def test_create_match_adds_the_creator_as_the_first_player(manager):
    result = create(manager, name="Izzy")

    match = manager.get_match(result.match_id)
    assert [player.name for player in match.players.values()] == ["Izzy"]
    assert result.player_id in match.players


def test_create_match_uses_default_word_count_when_omitted(manager):
    result = create(manager)

    words = manager.get_match(result.match_id).config.word_sequence
    assert len(words) == DEFAULT_WORD_COUNT


@pytest.mark.parametrize(
    "word_count",
    [
        pytest.param(1, id="[BVA] smallest"),
        pytest.param(7, id="[EP] typical"),
        pytest.param(40, id="[BVA] largest"),
    ],
)
def test_create_match_uses_requested_word_count(manager, word_count):
    result = create(manager, word_count=word_count)

    words = manager.get_match(result.match_id).config.word_sequence
    assert len(words) == word_count


def test_create_match_never_repeats_a_word(manager):
    result = create(manager, word_count=40)

    words = manager.get_match(result.match_id).config.word_sequence
    assert len(set(words)) == len(words)


def test_create_match_only_uses_words_from_the_answer_list(manager):
    result = create(manager, word_count=40)

    words = manager.get_match(result.match_id).config.word_sequence
    assert set(words) <= set(ANSWER_WORDS)


def test_create_match_uses_config_default_duration_when_omitted(manager):
    result = create(manager)

    assert manager.get_match(result.match_id).config.duration_seconds == 180


def test_create_match_honors_chosen_duration(manager):
    result = create(manager, duration_seconds=300)

    assert manager.get_match(result.match_id).config.duration_seconds == 300


def test_create_match_code_has_expected_length_and_characters(manager):
    code = create(manager).match_id

    assert len(code) == CODE_LENGTH
    assert set(code) <= set(CODE_ALPHABET)


def test_create_match_codes_are_unique_across_many_matches(manager):
    codes = {create(manager).match_id for _ in range(200)}

    assert len(codes) == 200


def test_generate_code_retries_when_a_code_is_already_taken(manager, monkeypatch):
    """[Other] A collision is skipped instead of overwriting an existing match."""
    existing = create(manager).match_id
    # generate_code draws one character at a time. Feed it the existing code
    # first (a collision), then a free one.
    characters = iter(existing + "FRESH1")
    monkeypatch.setattr(
        "server.match_manager.secrets.choice", lambda _alphabet: next(characters)
    )

    assert manager.generate_code() == "FRESH1"


def test_create_match_gives_the_player_an_unguessable_looking_id(manager):
    ids = {create(manager).player_id for _ in range(50)}

    assert len(ids) == 50
    assert all(len(player_id) >= 16 for player_id in ids)


def test_join_match_adds_the_second_player(manager):
    created = create(manager, name="Izzy")

    joined = join(manager, created.match_id, name="Sam")

    match = manager.get_match(created.match_id)
    assert [player.name for player in match.players.values()] == ["Izzy", "Sam"]
    assert joined.player_id in match.players
    assert joined.player_id != created.player_id


def test_join_match_second_player_moves_status_to_countdown(manager):
    created = create(manager)

    joined = join(manager, created.match_id)

    assert joined.status == MatchStatus.COUNTDOWN
    assert manager.get_match(created.match_id).status == MatchStatus.COUNTDOWN


def test_join_match_ignores_code_case_and_whitespace(manager):
    created = create(manager)

    joined = join(manager, f"  {created.match_id.lower()}  ")

    assert joined.match_id == created.match_id


def test_join_match_returns_the_canonical_match_id(manager):
    created = create(manager)

    joined = join(manager, created.match_id.lower())

    assert joined.match_id == created.match_id


def test_join_unknown_match_raises_not_found(manager):
    with pytest.raises(MatchNotFoundError):
        join(manager, "NOPE00")


def test_join_full_match_raises_match_full(manager):
    created = create(manager)
    join(manager, created.match_id)

    with pytest.raises(MatchFullError):
        join(manager, created.match_id, name="Third")


def test_join_active_match_raises_already_started(manager):
    created = create(manager)
    manager.get_match(created.match_id).status = MatchStatus.ACTIVE

    with pytest.raises(MatchAlreadyStartedError):
        join(manager, created.match_id)


def test_join_finished_match_raises_match_finished(manager):
    created = create(manager)
    manager.get_match(created.match_id).status = MatchStatus.FINISHED

    with pytest.raises(MatchFinishedError):
        join(manager, created.match_id)


def test_failed_join_does_not_add_a_player(manager):
    created = create(manager)
    join(manager, created.match_id)

    with pytest.raises(MatchFullError):
        join(manager, created.match_id, name="Third")

    match = manager.get_match(created.match_id)
    assert len(match.players) == MAX_PLAYERS
    assert "Third" not in [player.name for player in match.players.values()]


def test_finished_check_comes_before_started_check(manager):
    """[Other] A finished match reports 'finished', not 'already started'."""
    created = create(manager)
    manager.get_match(created.match_id).status = MatchStatus.FINISHED

    with pytest.raises(MatchFinishedError):
        join(manager, created.match_id)


def test_started_check_comes_before_full_check(manager):
    """[Other] A full match that is already active reports 'already started'."""
    created = create(manager)
    join(manager, created.match_id)  # now full, status countdown
    manager.get_match(created.match_id).status = MatchStatus.ACTIVE

    with pytest.raises(MatchAlreadyStartedError):
        join(manager, created.match_id, name="Third")


def test_finished_check_comes_before_full_check(manager):
    """[Other] A full match that is finished reports 'finished', not 'full'."""
    created = create(manager)
    join(manager, created.match_id)
    manager.get_match(created.match_id).status = MatchStatus.FINISHED

    with pytest.raises(MatchFinishedError):
        join(manager, created.match_id, name="Third")


def test_get_match_finds_an_existing_match(manager):
    created = create(manager)

    assert manager.get_match(created.match_id).config.match_id == created.match_id


@pytest.mark.parametrize(
    "transform",
    [
        pytest.param(str.lower, id="[EP] lowercase"),
        pytest.param(lambda code: f"  {code}  ", id="[EP] surrounding whitespace"),
        pytest.param(lambda code: f"\t{code.lower()}\n", id="[EP] both"),
    ],
)
def test_get_match_normalizes_the_code(manager, transform):
    created = create(manager)

    assert manager.get_match(transform(created.match_id)).config.match_id == (
        created.match_id
    )


@pytest.mark.parametrize(
    "code",
    [
        pytest.param("NOPE00", id="[EP] well-formed but unknown"),
        pytest.param("", id="[BVA] empty"),
        pytest.param("   ", id="[BVA] whitespace only"),
    ],
)
def test_get_match_unknown_code_raises_not_found(manager, code):
    with pytest.raises(MatchNotFoundError):
        manager.get_match(code)


def test_two_matches_keep_separate_players_and_words(manager):
    first = create(manager, name="Izzy", word_count=10)
    second = create(manager, name="Sam", word_count=10)

    join(manager, first.match_id, name="Alex")

    first_match = manager.get_match(first.match_id)
    second_match = manager.get_match(second.match_id)
    assert len(first_match.players) == 2
    assert len(second_match.players) == 1
    assert second_match.status == MatchStatus.WAITING


@pytest.mark.parametrize(
    ("error", "status_code", "error_name"),
    [
        (MatchNotFoundError, 404, "match_not_found"),
        (MatchFullError, 409, "match_full"),
        (MatchAlreadyStartedError, 409, "match_already_started"),
        (MatchFinishedError, 409, "match_finished"),
    ],
)
def test_each_error_carries_its_http_contract(error, status_code, error_name):
    exc = error()

    assert isinstance(exc, AppError)
    assert exc.status_code == status_code
    assert exc.error_name == error_name
    assert exc.message
    assert str(exc) == exc.message