import sys

import pygame


class EventBus:
    _subscribers = {}

    @classmethod
    def subscribe(cls, subtype, callback):
        if subtype in cls._subscribers:
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

    @classmethod
    def post(cls, event_type, **kwargs):
        event = pygame.event.Event(event_type, kwargs)
        pygame.event.post(event)

    @classmethod
    def process_events(cls):
        events = pygame.event.get()
        for event in events:
            if event.type in cls._subscribers:
                for callback in cls._subscribers[event.type]:
                    callback(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


class GameEvents:
    PLAYER_LOGIC_EVENT = pygame.USEREVENT + 1

    SUBTYPE_HIT = "hit"
