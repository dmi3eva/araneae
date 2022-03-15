from typing import *
from dataclasses import dataclass

from verification.src.controller import *
from verification.settings.content import *
from verification.settings.panels_inline import *
from verification.src.sender import *
from telebot import types


@dataclass
class Position:
    current: Optional[Status] = None
    panel: Optional[types.InlineKeyboardMarkup] = None
    transitions: Optional[Dict[str, Status]] = None
    generate_text: Optional[Callable] = None



POSITIONS = {
    Status.READY: Position(
        current=Status.READY,
        panel=info_panel,
        transitions={
            ESTIMATE: Status.IN_PROGRESS_FLUENCY_SOURCE,
        },
        generate_text=lambda controller, user: INSTRUCTIONS
    ),
    Status.IN_PROGRESS_FLUENCY_SOURCE: Position(
        current=Status.IN_PROGRESS_FLUENCY_SOURCE,
        panel=fluency_source_panel,
        transitions={
            CALL_OK: Status.IN_PROGRESS_FLUENCY_SUBSTITUTION,
            CALL_WRONG: Status.ERROR_DESCRIBING_FLUENCY_SOURCE,
            CALL_SKIP: Status.READY,
            CALL_DB: Status.DB_EXPLORING,
            CALL_INFO: Status.INFO_READING
        },
        generate_text=lambda controller, user: generate_fluency_source(controller, user)
    ),
    Status.IN_PROGRESS_FLUENCY_SUBSTITUTION: Position(
        current=Status.IN_PROGRESS_FLUENCY_SUBSTITUTION,
        panel=fluency_substitution_panel,
        transitions={
            CALL_OK: Status.IN_PROGRESS_EQUIVALENT,
            CALL_WRONG: Status.ERROR_DESCRIBING_FLUENCY_SUBSTITUTION,
            CALL_SKIP: Status.READY,
            CALL_DB: Status.DB_EXPLORING,
            CALL_INFO: Status.INFO_READING
        }
    ),
    Status.IN_PROGRESS_EQUIVALENT: Position(
        current=Status.IN_PROGRESS_EQUIVALENT,
        panel=equivalent_panel,
        transitions={
            CALL_OK: Status.IN_PROGRESS_SQL,
            CALL_WRONG: Status.ERROR_DESCRIBING_EQUIVALENT,
            CALL_SKIP: Status.READY,
            CALL_DB: Status.DB_EXPLORING,
            CALL_INFO: Status.INFO_READING
        }
    ),
    Status.IN_PROGRESS_SQL: Position(
        current=Status.IN_PROGRESS_SQL,
        panel=sql_panel,
        transitions={
            CALL_OK: Status.READY,
            CALL_WRONG: Status.ERROR_DESCRIBING_SQL,
            CALL_SKIP: Status.READY,
            CALL_DB: Status.DB_EXPLORING,
            CALL_INFO: Status.INFO_READING
        }
    )
}


TEXT_STATE_MAP = {
    # Status.ERROR_DESCRIBING_FLUENCY: Status.IN_PROGRESS_EQUIVALENT,
    # Status.ERROR_DESCRIBING_EQUIVALENT: Status.IN_PROGRESS_SQL,
    # Status.ERROR_DESCRIBING_SQL: Status.ERROR_DESCRIBING_EQUIVALENT
}
