"""Security must not break the product: the defended app still answers real questions."""

from __future__ import annotations

from secure_rag.app import USERS, RagApp
from secure_rag.defenses import DEFENDED, NOT_FOUND
from secure_rag.llm import GullibleFakeLLM


def defended():
    return RagApp(GullibleFakeLLM(), DEFENDED)


def test_answers_with_citation():
    result = defended().ask(USERS["alice"], "How many unused leave days can be carried over?")
    assert result.answer == "Up to 5 unused days can be carried over into the next year. [acme-leave]"


def test_each_tenant_gets_its_own_policy():
    app = defended()
    assert "24 days" in app.ask(USERS["alice"], "How many paid leave days per year?").answer
    assert "20 days" in app.ask(USERS["bob"], "How many paid leave days per year?").answer


def test_says_not_found_instead_of_guessing():
    assert defended().ask(USERS["alice"], "What is the parking policy?").answer == NOT_FOUND


def test_poisoned_documents_are_quarantined_for_review():
    assert set(defended().quarantined) == {"acme-wfh", "acme-it"}


def test_quarantined_documents_are_never_retrieved():
    result = defended().ask(USERS["alice"], "Can I work from home?")
    assert "acme-wfh" not in result.sources
