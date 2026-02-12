import sys
from typing import Callable, Any

import pygame


class EventBus:
    _subscribers = {}

    @classmethod
    def subscribe(cls, subtype: str, callback: Callable[[Any], None]):
        if subtype not in cls._subscribers:
            cls._subscribers[subtype] = []

        if callback not in cls._subscribers[subtype]:
            cls._subscribers[subtype].append(callback)

    @classmethod
    def unsubscribe(cls, event_type, callback):
        if event_type in cls._subscribers:
            try:
                cls._subscribers[event_type].remove(callback)

                if not cls._subscribers[event_type]:
                    del cls._subscribers[event_type]
            except ValueError:
                pass

    @staticmethod
    def post(eventy_type, **kwargs):
        event = pygame.event.Event(eventy_type, kwargs)
        pygame.event.post(event)

    @classmethod
    def process_events(cls):
        for event in pygame.event.get():
            if event.type in cls._subscribers:
                for callback in cls._subscribers[event.type]:
                    callback(event)

            subtype = getattr(event, "subtype", None)
            if subtype and subtype in cls._subscribers:
                for callback in list(cls._subscribers[subtype]):
                    callback(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


class GameEvents:
    PLAYER_LOGIC_EVENT = pygame.USEREVENT + 1

    SUBTYPE_ACTION_MOVE = "action_move"
    SUBTYPE_ACTION_SHOOT = "SHOOT"
