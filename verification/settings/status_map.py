from typing import *
from dataclasses import dataclass

from verification.src.controller import *
from verification.settings.content import *
from verification.settings.panels_inline import *
from verification.src.sender import *
from verification.src.error_handlers import *
from telebot import types


@dataclass
class Position:
    current: Optional[Status] = None
    panel: Optional[Callable] = None
    transitions: Optional[Dict[str, Status]] = None
    generate_text: Optional[Callable] = None
    handle_error: Optional[Callable] = None


POSITIONS = {
    Status.READY: Position(
        current=Status.READY,
        panel=lambda sample: info_panel,
        transitions={
            ESTIMATE: Status.IN_PROGRESS_FLUENCY_SOURCE,
        },
        generate_text=lambda controller, user: INSTRUCTIONS,
        handle_error=lambda user, sample, correction: save_sql_correct(user, sample, correction)
    ),
    Status.IN_PROGRESS_FLUENCY_SOURCE: Position(
        current=Status.IN_PROGRESS_FLUENCY_SOURCE,
        panel=lambda sample: fluency_source_panel,
        transitions={
            CALL_OK: Status.IN_PROGRESS_FLUENCY_SUBSTITUTION,
            CALL_WRONG: Status.ERROR_DESCRIBING_FLUENCY_SOURCE,
            CALL_SKIP: Status.IN_PROGRESS_FLUENCY_SOURCE,
            CALL_DB: Status.CHOOSING_TABLE,
            CALL_INFO: Status.INFO_READING
        },
        generate_text=lambda controller, user: generate_fluency_source_msg(controller, user),
        handle_error=lambda user, sample, correction: sample
    ),
    Status.IN_PROGRESS_FLUENCY_SUBSTITUTION: Position(
        current=Status.IN_PROGRESS_FLUENCY_SUBSTITUTION,
        panel=lambda sample: fluency_substitution_panel,
        transitions={
            CALL_OK: Status.IN_PROGRESS_EQUIVALENT,
            CALL_WRONG: Status.ERROR_DESCRIBING_FLUENCY_SUBSTITUTION,
            CALL_SKIP: Status.IN_PROGRESS_FLUENCY_SOURCE,
            CALL_DB: Status.CHOOSING_TABLE,
            CALL_INFO: Status.INFO_READING
        },
        generate_text=lambda controller, user: generate_fluency_substitution_msg(controller, user),
        handle_error=lambda user, sample, correction: save_fluency_source_correct(user, sample, correction)
    ),
    Status.IN_PROGRESS_EQUIVALENT: Position(
        current=Status.IN_PROGRESS_EQUIVALENT,
        panel=lambda sample: equivalent_panel,
        transitions={
            CALL_OK: Status.IN_PROGRESS_SQL,
            CALL_WRONG: Status.ERROR_DESCRIBING_EQUIVALENT,
            CALL_SKIP: Status.IN_PROGRESS_FLUENCY_SOURCE,
            CALL_DB: Status.CHOOSING_TABLE,
            CALL_INFO: Status.INFO_READING
        },
        generate_text=lambda controller, user: generate_equivalent_msg(controller, user),
        handle_error=lambda user, sample, correction: save_fluency_substitution_correct(user, sample, correction)
    ),
    Status.IN_PROGRESS_SQL: Position(
        current=Status.IN_PROGRESS_SQL,
        panel=lambda sample: sql_panel,
        transitions={
            CALL_OK: Status.IN_PROGRESS_FLUENCY_SOURCE,
            CALL_WRONG: Status.ERROR_DESCRIBING_SQL,
            CALL_SKIP: Status.IN_PROGRESS_FLUENCY_SOURCE,
            CALL_DB: Status.CHOOSING_TABLE,
            CALL_INFO: Status.INFO_READING
        },
        generate_text=lambda controller, user: generate_sql_msg(controller, user),
        handle_error=lambda user, sample, correction: save_equivalent_correct(user, sample, correction)
    ),
    Status.ERROR_DESCRIBING_FLUENCY_SOURCE: Position(
        current=Status.ERROR_DESCRIBING_FLUENCY_SOURCE,
        panel=lambda sample: error_fluency_source_panel,
        transitions={
            CALL_SKIP: Status.READY,
            CALL_INFO: Status.INFO_READING,
            TEXT_TYPED: Status.IN_PROGRESS_FLUENCY_SUBSTITUTION
        },
        generate_text=lambda controller, user: generate_error_fluency_source_msg(controller, user),
        handle_error=lambda user, sample, correction: save_fluency_source_error(user, sample, correction)
    ),
    Status.ERROR_DESCRIBING_FLUENCY_SUBSTITUTION: Position(
        current=Status.ERROR_DESCRIBING_FLUENCY_SUBSTITUTION,
        panel=lambda sample: error_fluency_substitution_panel,
        transitions={
            CALL_SKIP: Status.READY,
            CALL_INFO: Status.INFO_READING,
            TEXT_TYPED: Status.IN_PROGRESS_EQUIVALENT
        },
        generate_text=lambda controller, user: generate_error_fluency_substitution_msg(controller, user),
        handle_error=lambda user, sample, correction: save_fluency_substitution_error(user, sample, correction)
    ),
    Status.ERROR_DESCRIBING_EQUIVALENT: Position(
        current=Status.ERROR_DESCRIBING_EQUIVALENT,
        panel=lambda sample: error_equivalent_panel,
        transitions={
            CALL_SKIP: Status.READY,
            CALL_INFO: Status.INFO_READING,
            TEXT_TYPED: Status.IN_PROGRESS_EQUIVALENT
        },
        generate_text=lambda controller, user: generate_error_equivalent_msg(controller, user),
        handle_error=lambda user, sample, correction: save_equivalent_error(user, sample, correction)
    ),
    Status.ERROR_DESCRIBING_SQL: Position(
        current=Status.ERROR_DESCRIBING_SQL,
        panel=lambda sample: error_sql_panel,
        transitions={
            CALL_SKIP: Status.READY,
            CALL_INFO: Status.INFO_READING,
            TEXT_TYPED: Status.IN_PROGRESS_EQUIVALENT
        },
        generate_text=lambda controller, user: generate_error_sql_msg(controller, user),
        handle_error=lambda user, sample, correction: save_sql_error(user, sample, correction)
    ),
    Status.INFO_READING: Position(
        current=Status.INFO_READING,
        panel=lambda sample: in_progress_info_panel,
        transitions={
            RETURN: Status.LAST,
        },
        generate_text=lambda controller, user: INSTRUCTIONS,
        handle_error=lambda user, sample, correction: sample
    ),
    Status.CHOOSING_TABLE: Position(
        current=Status.CHOOSING_TABLE,
        panel=lambda sample: generate_tables_panel(sample),
        transitions={
            RETURN: Status.LAST,
            TABLE: Status.VIEW_TABLE
        },
        generate_text=lambda controller, user: generate_choosing_table(controller, user),
        handle_error=lambda user, sample, correction: sample
    ),
    Status.VIEW_TABLE: Position(
        current=Status.VIEW_TABLE,
        panel=lambda sample: view_panel,
        transitions={
            RETURN_TO_TABLES: Status.CHOOSING_TABLE,
            RETURN: Status.LAST
        },
        generate_text=lambda controller, user: generate_view_table_msg(controller, user),
        handle_error=lambda user, sample, correction: sample
    )
}


TEXT_STATE_MAP = {
    # Status.ERROR_DESCRIBING_FLUENCY: Status.IN_PROGRESS_EQUIVALENT,
    # Status.ERROR_DESCRIBING_EQUIVALENT: Status.IN_PROGRESS_SQL,
    # Status.ERROR_DESCRIBING_SQL: Status.ERROR_DESCRIBING_EQUIVALENT
}
