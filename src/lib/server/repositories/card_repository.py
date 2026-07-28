from ..data_loader import get_cards
from ..game_types import CardDescription, CardId


class CardNotFoundException(Exception):
    def __init__(self, card_id: CardId):
        super().__init__(f"Card with card_id {card_id} not found.")


class CardRepository:
    """Repository for loading and querying card descriptions."""

    def __init__(self):
        self._cards_by_id: dict[CardId, CardDescription] = {}
        self._loaded = False

    def _load(self) -> None:
        if self._loaded:
            return

        cards = get_cards()
        self._cards_by_id = {card.id: card for card in cards}
        self._loaded = True

    def get_by_id(self, card_id: CardId) -> CardDescription:
        """Return a single card description by id."""
        self._load()
        card_description = self._cards_by_id.get(card_id)
        if not card_description:
            raise CardNotFoundException(card_id)
        return card_description

    def get_all_ids(self) -> list[CardId]:
        """
        Return a list of card id objects
        """
        self._load()
        return list(self._cards_by_id.keys())


card_repository = CardRepository()
