import pytest

from aphra_blogger.agents.anonymous_blogger import (
    AnonymousBloggerEmulator,
    AnonymousProfile,
    make_disclaimer,
)


def test_load_profile_bloggeranon():
    ev = AnonymousBloggerEmulator()
    p = ev.load_profile("BloggerAnon")
    assert isinstance(p, AnonymousProfile)
    assert p.alias == "BloggerAnon"


def test_apply_profile_to_prompt_includes_style():
    ev = AnonymousBloggerEmulator()
    p = ev.load_profile("BloggerAnon")
    base = "Escribe sobre IA en 500 palabras"
    enriched = ev.apply_profile_to_prompt(base, p)
    assert "Estilo: BloggerAnon" in enriched


def test_disclaimer_generation():
    p = AnonymousProfile(
        alias="BloggerAnon",
        bio="desc",
        tone="neutral",
        vocabulary=["tech"],
        topics=["IA"],
        disclaimer_template="Este contenido fue generado por IA y simula la voz de BloggerAnon (anon)",
    )
    text = make_disclaimer(p)
    assert "BloggerAnon" in text
