import random
import secrets
import string
from dataclasses import dataclass

from game_engine.models import Match, MatchConfig, MatchStatus, PlayerState
from game_engine.word_list import load_answer_words
from server.schemas import CreateMatchRequest, JoinMatchRequest

from .exceptions import (
    MatchAlreadyStartedError,
    MatchFinishedError,
    MatchFullError,
    MatchNotFoundError,
)

CODE_LENGTH = 6
CODE_ALPHABET = string.ascii_uppercase + string.digits

DEFAULT_WORD_COUNT = 10

MAX_PLAYERS = 2


@dataclass(frozen=True)
class JoinResult:
    """What create_match and join_match hand back to the caller."""

    match_id: str
    player_id: str
    status: MatchStatus


class MatchManager:
    def __init__(self, answer_words: list[str] | None = None) -> None:
        self._matches: dict[str, Match] = {}
        # Passing a word list in keeps tests small and avoids reading the
        # file on every create.
        self._answer_words = (
            answer_words if answer_words is not None else load_answer_words()
        )
        # SystemRandom draws from the OS, so a player cannot predict the
        # words from earlier output the way they could with a seeded RNG.
        self._rng = random.SystemRandom()

    def create_match(
        self,
        data: CreateMatchRequest,
    ) -> JoinResult:
        """Create a match with its first player (the creator)."""
        word_count = data.word_count
        if word_count is None:
            word_count = DEFAULT_WORD_COUNT

        # sample() never repeats a word within one match.
        word_sequence = self._rng.sample(self._answer_words, k=word_count)

        config_kwargs = {
            "match_id": self.generate_code(),
            "word_sequence": word_sequence,
        }
        # Leave duration out when not given so MatchConfig's default applies.
        if data.duration_seconds is not None:
            config_kwargs["duration_seconds"] = data.duration_seconds

        match = Match(config=MatchConfig(**config_kwargs))
        player = self.add_player(match, data.name)
        self._matches[match.config.match_id] = match
        
        return JoinResult(match.config.match_id, player.player_id, match.status)


    def join_match(self, code: str, data: JoinMatchRequest) -> JoinResult:
        """Add a player to an existing match.

        Checks run in this order: exists, finished, started, full.
        """
        match = self.get_match(code)  # raises MatchNotFoundError

        if match.status == MatchStatus.FINISHED:
            raise MatchFinishedError()
        if match.status == MatchStatus.ACTIVE:
            raise MatchAlreadyStartedError()
        if len(match.players) >= MAX_PLAYERS:
            raise MatchFullError()

        player = self.add_player(match, data.name)

        if len(match.players) == MAX_PLAYERS:
            match.status = MatchStatus.COUNTDOWN

        return JoinResult(match.config.match_id, player.player_id, match.status)


    def get_match(self, code: str) -> Match:
        """Find a match by code, ignoring case and surrounding whitespace.

        Every caller goes through here, so code normalization lives in one place.
        """
        match = self._matches.get(code.strip().upper())
        if match is None:
            raise MatchNotFoundError()
        return match


    def add_player(self, match: Match, name: str) -> PlayerState:
        # token_urlsafe is unguessable; a guessable ID would let someone act
        # as another player.
        player = PlayerState(player_id=secrets.token_urlsafe(), name=name)
        match.players[player.player_id] = player
        return player


    def generate_code(self) -> str:
        """Make an unguessable match code, retrying on the rare collision."""
        while True:
            code = "".join(secrets.choice(CODE_ALPHABET) for _ in range(CODE_LENGTH))
            if code not in self._matches:
                return code