import logging
from abc import ABC

from errloom.synapseware.synaphor import Synaphor
from errloom.synapseware.synapseware import Synapseware, ClassSpan
from errloom.tapestry import Rollout
from errloom.lib import log
from tests.base import ErrloomTest
from errloom.synapseware.synapseware import TextSpan

logger = log.getLogger(__name__)

# Mock classes for testing
# ----------------------------------------

class MockLoom:
    def __init__(self, sample_text="mocked_sample"):
        self.sample_text = sample_text

    def sample(self, rollout, stop_sequences=[]):
        return self.sample_text


class SynapseClass:
    """A versatile mock class for testing synapseware execution."""
    def __init__(self, *kargs, **kwargs):
        self.init_args = (kargs, kwargs)
        self.init_called = True
        self.synapse_init_called = False
        self.synapse_end_called = False
        self.synapse_called = False
        self.last_synapse_args = None
        self.last_synapse_init_args = None
        self.last_synapse_end_args = None

    def __synapse_init__(self, synaphor, span):
        self.synapse_init_called = True
        self.last_synapse_init_args = (synaphor, span)

    def __synapse__(self, synaphor, span):
        self.synapse_called = True
        self.last_synapse_args = (synaphor, span)
        return f"Synapse! kargs={span.kargs}, kwargs={span.kwargs}"

    def __synapse_end__(self, synaphor, span):
        self.synapse_end_called = True
        self.last_synapse_end_args = (synaphor, span)


class SynapseTest(ErrloomTest, ABC):
    def setUp(self) -> None:
        super().setUp()
        self.loom = MockLoom()
        self.env = {
            "SynapseTest": SynapseClass,
            "my_var": "injected_value",
        }
        self.synapseware: Synapseware | None = None
        self.synaphor: Synaphor | None = None
        self.rollout: Rollout | None = None

    def run_synapseware(self, code: str) -> tuple[Synapseware, Synaphor]:
        """Helper function to parse and run a synapseware string."""
        synapseware = Synapseware.parse(code)
        logger.info("=== PARSED: ===")
        logger.info(synapseware.to_rich())

        self.synapseware = synapseware
        self.rollout = Rollout(row={})
        self.synaphor = Synaphor(loom=self.loom, rollout=self.rollout, env=self.env)
        setattr(self.synaphor, "dry", True)

        logging.getLogger().setLevel(logging.DEBUG)

        logger.info("=== EXECUTING: ===")
        synapseware(self.synaphor)

        logger.info("=== RESULT: ===")
        self.rollout.to_api_chat()
        logging.getLogger().setLevel(logging.INFO)
        logger.info(self.rollout.to_rich())

        return synapseware, self.synaphor


# Tests
# ----------------------------------------

class SynapsewareExecutionTest(SynapseTest):
    def test_synapseware_run_simple_text(self):
        code = "Hello, world!"
        synapseware, synaphor = self.run_synapseware(code)

        self.assertEqual(len(synaphor.contexts), 1)
        context = synaphor.contexts[0]
        self.assertEqual(len(context.fragments), 1)
        self.assertEqual(context.fragments[0].text, "Hello, world!")

    def test_synapseware_run_ego_change(self):
        code = "<|o_o|>User message.<|@_@|>Assistant response."
        synapseware, synaphor = self.run_synapseware(code)

        self.assertEqual(len(synaphor.contexts), 1)
        context = synaphor.contexts[0]
        frags = context.fragments
        self.assertEqual(len(frags), 2)
        self.assertIn("User message.", frags[0].text)
        self.assertIn("Assistant response.", frags[1].text)
        self.assertEqual(synaphor._ego, "assistant")

    def test_synapseware_run_obj_span(self):
        code = "<|o_o|>Value is <|my_var|>."
        synapseware, synaphor = self.run_synapseware(code)

        self.assertEqual(len(synaphor.contexts), 1)
        context = synaphor.contexts[0]
        frags = context.fragments
        self.assertGreaterEqual(len(frags), 2)
        self.assertIn("<obj id=my_var>injected_value</obj>", "".join(f.text for f in frags))

    def test_synapseware_run_class_lifecycle(self):
        code = "<|o_o|><|SynapseTest|>"
        synapseware, synaphor = self.run_synapseware(code)

        self.assertEqual(len(synaphor.span_bindings), 1)
        instance = list(synaphor.span_bindings.values())[0]

        self.assertIsInstance(instance, SynapseClass)
        self.assertTrue(instance.init_called)
        self.assertTrue(instance.synapse_init_called)
        self.assertTrue(instance.synapse_called)
        self.assertTrue(instance.synapse_end_called)

        context = synaphor.contexts[0]
        frags = context.fragments
        self.assertGreaterEqual(len(frags), 1)
        self.assertTrue(any("Synapse! kargs=[], kwargs={}" in f.text for f in frags))

    def test_synapseware_run_class_with_args(self):
        code = "<|o_o|><|SynapseTest karg1 karg2 key1=val1|>"
        synapseware, synaphor = self.run_synapseware(code)

        instance = list(synaphor.span_bindings.values())[0]

        self.assertEqual(instance.init_args[0], ("karg1", "karg2"))
        self.assertEqual(instance.init_args[1], {"key1": "val1"})

        self.assertIsInstance(instance.last_synapse_init_args[0], Synaphor)
        self.assertIsInstance(instance.last_synapse_init_args[1], ClassSpan)

        self.assertIsInstance(instance.last_synapse_args[0], Synaphor)
        self.assertIsInstance(instance.last_synapse_args[1], ClassSpan)

        self.assertIsInstance(instance.last_synapse_end_args[0], Synaphor)
        self.assertIsInstance(instance.last_synapse_end_args[1], ClassSpan)

    def test_synapseware_run_sample_span(self):
        code = "<|@_@ <>test|>"
        synapseware, synaphor = self.run_synapseware(code)

        context = synaphor.contexts[0]
        frags = context.fragments

        self.assertGreaterEqual(len(frags), 1)
        self.assertTrue(any(f.text == "<test>" for f in frags))
        self.assertTrue(any(f.text == "mocked_sample</test>" for f in frags))

    def test_data_assignment_across_contexts(self):
        code = (
            "<|+++|>"
            "<|o_o|>Source.\n"
            "<|@_@:compressed <>compress|>"
            "<|+++|>"
            "<|o_o|>Injected: <|compressed|>"
        )
        synapseware, synaphor = self.run_synapseware(code)

        self.assertIn('compressed', synaphor.env)
        self.assertEqual(synaphor.env['compressed'], "mocked_sample")

        self.assertEqual(len(synaphor.contexts), 2)
        context1_content = "".join(frag.text for frag in synaphor.contexts[1].fragments)
        self.assertIn("<obj id=compressed>mocked_sample</obj>", context1_content)
