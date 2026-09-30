import sys
from core.tools.gmail_tools import INBOX_READER_TOOLS, MAIL_SEARCHER_TOOLS, CALENDAR_TOOLS, DRAFT_WRITER_TOOLS
from core.prompts.prompt_factory import PromptContext, build_subagent_description, build_subagent_prompt
from utils.model_loader import ModelLoader
from exception.custom_exception import EmailCustomException
from logger.custom_logger import EmailCustomLogger

logger = EmailCustomLogger().get_logger(__file__)

SUBAGENT_TOOLS = {
    "inbox-reader": INBOX_READER_TOOLS,
    "mail-searcher": MAIL_SEARCHER_TOOLS,
    "calendar-agent": CALENDAR_TOOLS,
    "draft-writer": DRAFT_WRITER_TOOLS,
}

try:
    loader = ModelLoader()
    model = loader.groq
except Exception as e:
    raise EmailCustomException(e, sys) from e


def build_subagents(ctx: PromptContext | None = None, model: str | None = model) -> list[dict]:
    """Build subagent dicts; prompts come from the prompt factory, model=None inherits the main agent's."""
    try:
        logger.info("building_subagents", ctx=str(ctx), model=model)
        subagents = []
        for name, tools in SUBAGENT_TOOLS.items():
            spec = {
                "name": name,
                "description": build_subagent_description(name, ctx),
                "system_prompt": build_subagent_prompt(name, ctx),
                "tools": tools,
            }
            if model:
                spec["model"] = model
            subagents.append(spec)
        logger.info("subagents_built", count=len(subagents))
        return subagents
    except Exception as e:
        raise EmailCustomException(e, sys) from e
