import itertools

import pytest
from fastapi.testclient import TestClient

from server.dependencies import get_match_manager
from server.main import app
from server.match_manager import MatchManager

# Why create this instead of read from the real one?
# Because the real words will change, this way we know the words and also it's faster
ANSWER_WORDS = [
    "".join(letters)
    for letters in itertools.islice(itertools.product("ABCDEFGHIJ", repeat=5), 50)
]

CREATE_RESPONSE_KEYS = {"match_id", "player_id", "status"}
ERROR_RESPONSE_KEYS = {"error_name", "message"}
STATE_RESPONSE_KEYS = {
    "match_id",
    "status",
    "player_count",
    "player_names",
    "guess_limit",
    "duration_seconds",
}


@pytest.fixture
def manager():
    """A fresh MatchManager with a small, known word list."""
    return MatchManager(answer_words=ANSWER_WORDS)

@pytest.fixture
def client(manager):
    """A TestClient whose app uses the fresh manager."""
    app.dependency_overrides[get_match_manager] = lambda: manager
    yield TestClient(app)

    # Clear after test runs
    app.dependency_overrides.clear()


def valid_match_data() -> dict:
    """A request body that passes validation."""
    return {"name":"Izzy"}


def create_match(client, **changes):
    """POST /matches with valid data, optionally overriding fields."""
    return client.post("/matches", json={**valid_match_data(), **changes})


def join_match(client, match_id, name="Sam"):
    return client.post(f"/matches/{match_id}/players", json={"name":name})


# POST /matches

def test_create_match_returns_201_with_expected_fields(client):
    response = create_match(client)

    assert response.status_code == 201
    body = response.json()
    assert set(body) == CREATE_RESPONSE_KEYS
    assert body["status"] == "waiting"


def test_create_match_does_not_expose_word_sequence(client):
    body = create_match(client).json()

    assert "word_sequence" not in body

# What is parametrize? this is for running a function multiple times w/ different data
# So this would run 6 times, each time is it's own test
@pytest.mark.parametrize(
    "changes",
    [
        pytest.param({"duration_seconds": 60}, id="[BVA] shortest duration"),
        pytest.param({"duration_seconds": 300}, id="[BVA] longest duration"),
        pytest.param({"word_count": 1}, id="[BVA] smallest word count"),
        pytest.param({"word_count": 40}, id="[BVA] largestest word count"),
        pytest.param({"name": "A"}, id="[BVA] 1-character name"),
        pytest.param({"name": "A" * 20}, id="[BVA] 20-character name"),
    ]
)

def test_create_match_accepts_boundary_values(client, changes):
    assert create_match(client, **changes).status_code == 201

    
@pytest.mark.parametrize(
    "changes",
    [
        pytest.param({"duration_seconds": 90}, id="[EP] duration not in allowed list"),
        pytest.param({"duration_seconds": 0}, id="[BVA] duration zero"),
        pytest.param({"word_count": 0}, id="[BVA] word count below minimum"),
        pytest.param({"word_count": 41}, id="[BVA] word count above maximum"),
        pytest.param({"name": ""}, id="[BVA] empty name"), # Why bva, why below ep?
        pytest.param({"name": "   "}, id="[EP] spaces-only name"),
        pytest.param({"name": "A" * 21}, id="[BVA] 21-character name"),
        pytest.param({"unexpected": 1}, id="[EP] unknown field"),
    ],
)
def test_create_match_rejects_invalid_input(client, changes):
    assert create_match(client, **changes).status_code == 422
 
 
def test_create_match_without_a_name_returns_422(client):
    assert client.post("/matches", json={}).status_code == 422
 
 
def test_create_match_without_a_body_returns_422(client):
    assert client.post("/matches").status_code == 422
 
 
def test_create_match_uses_default_duration_when_omitted(client):
    match_id = create_match(client).json()["match_id"]
 
    state = client.get(f"/matches/{match_id}").json()
    assert state["duration_seconds"] == 180
 
 
def test_create_match_uses_chosen_duration(client):
    match_id = create_match(client, duration_seconds=120).json()["match_id"]
 
    state = client.get(f"/matches/{match_id}").json()
    assert state["duration_seconds"] == 120
 
 
def test_create_match_picks_requested_number_of_words(client, manager):
    match_id = create_match(client, word_count=7).json()["match_id"]
 
    assert len(manager.get_match(match_id).config.word_sequence) == 7



 
# --- POST /matches/{match_id}/players ---------------------------------------
 
 
def test_join_match_returns_201_and_starts_countdown(client):
    match_id = create_match(client).json()["match_id"]
 
    response = join_match(client, match_id)
 
    assert response.status_code == 201
    body = response.json()
    assert set(body) == CREATE_RESPONSE_KEYS
    assert body["match_id"] == match_id
    assert body["status"] == "countdown"
 
 
def test_join_match_gives_each_player_a_different_id(client):
    created = create_match(client).json()
 
    joined = join_match(client, created["match_id"]).json()
 
    assert joined["player_id"] != created["player_id"]
 
 
def test_join_full_match_returns_409_match_full(client):
    match_id = create_match(client).json()["match_id"]
    join_match(client, match_id)
 
    response = join_match(client, match_id, name="Third")
 
    assert response.status_code == 409
    assert response.json()["error_name"] == "match_full"
 
 
def test_join_unknown_match_returns_404_match_not_found(client):
    response = join_match(client, "NOPE00")
 
    assert response.status_code == 404
    assert response.json()["error_name"] == "match_not_found"
 
 
@pytest.mark.parametrize(
    "body",
    [
        pytest.param({"name": ""}, id="[BVA] empty name"),
        pytest.param({"name": "A" * 21}, id="[BVA] 21-character name"),
        pytest.param({}, id="[EP] missing name"),
        pytest.param({"name": "Sam", "unexpected": 1}, id="[EP] unknown field"),
    ],
)
def test_join_match_rejects_invalid_input(client, body):
    match_id = create_match(client).json()["match_id"]
 
    response = client.post(f"/matches/{match_id}/players", json=body)
 
    assert response.status_code == 422
 
 
# --- GET /matches/{match_id} ------------------------------------------------
 
 
def test_get_match_returns_public_state(client):
    match_id = create_match(client, duration_seconds=120).json()["match_id"]
 
    response = client.get(f"/matches/{match_id}")
 
    assert response.status_code == 200
    body = response.json()
    assert set(body) == STATE_RESPONSE_KEYS
    assert body == {
        "match_id": match_id,
        "status": "waiting",
        "player_count": 1,
        "player_names": ["Izzy"],
        "guess_limit": 6,
        "duration_seconds": 120,
    }
 
 
def test_get_match_lists_names_in_join_order(client):
    match_id = create_match(client, name="Izzy").json()["match_id"]
    join_match(client, match_id, name="Sam")
 
    body = client.get(f"/matches/{match_id}").json()
 
    assert body["player_names"] == ["Izzy", "Sam"]
    assert body["player_count"] == 2
 
 
def test_get_match_code_is_case_insensitive(client):
    match_id = create_match(client).json()["match_id"]
 
    assert client.get(f"/matches/{match_id.lower()}").status_code == 200
 
 
def test_get_unknown_match_returns_404_match_not_found(client):
    response = client.get("/matches/NOPE00")
 
    assert response.status_code == 404
    assert response.json()["error_name"] == "match_not_found"


def test_match_state_never_leaks_secrets(client, manager):
    """[Other] No answer word and no player_id appears in the public state."""
    created = create_match(client).json()
    joined = join_match(client, created["match_id"]).json()
 
    text = client.get(f"/matches/{created['match_id']}").text
 
    assert "word_sequence" not in text
    assert created["player_id"] not in text
    assert joined["player_id"] not in text
    for word in manager.get_match(created["match_id"]).config.word_sequence:
        assert word not in text
 
 
def test_errors_use_the_documented_body_shape(client):
    body = client.get("/matches/NOPE00").json()
 
    assert set(body) == ERROR_RESPONSE_KEYS
 
 
def test_create_join_get_flow(client):
    """[Other] The whole Sprint 2 flow works end to end."""
    created = create_match(client, name="Izzy").json()
    assert created["status"] == "waiting"
 
    joined = join_match(client, created["match_id"], name="Sam").json()
    assert joined["status"] == "countdown"
 
    state = client.get(f"/matches/{created['match_id']}").json()
    assert state["player_count"] == 2
    assert state["player_names"] == ["Izzy", "Sam"]
    assert state["status"] == "countdown"
 
 
def test_matches_do_not_share_state(client):
    """[Other] Two matches running at once stay independent."""
    first = create_match(client, name="Izzy").json()["match_id"]
    second = create_match(client, name="Sam").json()["match_id"]
 
    join_match(client, first, name="Alex")
 
    assert client.get(f"/matches/{first}").json()["player_count"] == 2
    assert client.get(f"/matches/{second}").json()["player_count"] == 1