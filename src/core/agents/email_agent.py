import sys
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langgraph.checkpoint.memory import MemorySaver

from core.prompts.prompt_factory import PromptContext, build_main_prompt
from core.subagents.mail_subagents import build_subagents
from exception.custom_exception import EmailCustomException
from logger.custom_logger import EmailCustomLogger

logger = EmailCustomLogger().get_logger(__file__)


class EmailAgent:
    def __init__(self, ctx: PromptContext | None = None, subagent_model: str | None = None):
        try:
            logger.info("email_agent_init", ctx=str(ctx), subagent_model=subagent_model)
            self.be = FilesystemBackend(root_dir=".", virtual_mode=True)
            self.ms = MemorySaver()
            self.subagents = build_subagents(ctx, subagent_model)
            self.system_prompt = build_main_prompt(ctx)
            logger.info("email_agent_ready")
        except Exception as e:
            raise EmailCustomException(e, sys) from e

    def main_agent(self, response_format=None) -> create_deep_agent:
        try:
            logger.info("main_agent_building")
            agent = create_deep_agent(
                system_prompt=self.system_prompt,
                backend=self.be,
                checkpointer=self.ms,
                subagents=self.subagents,
                response_format=response_format,
            )
            logger.info("main_agent_ready")
            return agent
        except Exception as e:
            raise EmailCustomException(e, sys) from e
