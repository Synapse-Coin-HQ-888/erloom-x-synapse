from rich.rule import Rule

from errloom.lib import log
from errloom.tapestry import Rollout
from tests.base import ErrloomTest

logger = log.getLogger(__name__)


class LogAlignmentTests(ErrloomTest):
    def test_rule(self):
        logger.info(Rule(style="dim"))
        logger.info(Rule(style="cyan"))
        logger.info(Rule(style="red"))

    def test_rollout_conversation(self):
        roll = Rollout({})
        roll.new_context()
        roll.add_frozen("system", """
You are an expert in information theory and symbolic compression.
Your task is to compress text losslessly into a format unreadable by humans but optimized for maximum density.
Utilize language blending, abbreviations, and Unicode symbols to achieve extreme compression while preserving all information necessary for perfect reconstruction.
        """)
        roll.add_frozen(ego="user", content="Foo1")
        roll.add_frozen(ego="assistant", content="Bar2")
        roll.new_context()
        roll.add_frozen("system", "This remains a test scenario.")
        roll.add_frozen(ego="user", content="Foo1")
        roll.add_frozen(ego="assistant", content="Bar2")

        logger.info(roll.to_rich())
