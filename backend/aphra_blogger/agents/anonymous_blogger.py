from dataclasses import dataclass
from typing import List


@dataclass
class AnonymousProfile:
    alias: str
    bio: str
    tone: str
    vocabulary: List[str]
    topics: List[str]
    disclaimer_template: str


class AnonymousBloggerEmulator:
    def __init__(self):
        self.profiles = {
            "BloggerAnon": AnonymousProfile(
                alias="BloggerAnon",
                bio="Un blogger anonimo con voz genérica orientada a tecnología y actualidad.",
                tone="neutral",
                vocabulary=[
                    "punto",
                    "análisis",
                    "tecnología",
                    "AI",
                    "cloud",
                    "desarrollo",
                    "arquitectura",
                ],
                topics=["IA", "IA ética", "desarrollos tecnológicos", "cloud", "programación"],
                disclaimer_template="Este contenido fue generado por IA y simula la voz de BloggerAnon (anónimo); no representa a una persona real.",
            ),
            "TravelAnon": AnonymousProfile(
                alias="TravelAnon",
                bio="Un blogger anonimo centrado en viajes y experiencias culturales.",
                tone="informal",
                vocabulary=["destino", "viaje", "experiencia", "cultura", "gastronomía"],
                topics=["viajes", "turismo responsable", "destinos"],
                disclaimer_template="Este contenido fue generado por IA y simula la voz de TravelAnon (anoním@); no representa a una persona real.",
            ),
        }

    def load_profile(self, name: str) -> AnonymousProfile:
        return self.profiles.get(name) or self.profiles["BloggerAnon"]

    def apply_profile_to_prompt(self, base_prompt: str, profile: AnonymousProfile) -> str:
        # Enriquecer el prompt con indicaciones de estilo
        style_hint = (
            f"[Estilo: {profile.alias} | tono: {profile.tone} | temas: {', '.join(profile.topics)}]"
        )
        vocab_hint = " ".join(profile.vocabulary)
        enriched = f"{style_hint} {base_prompt} {vocab_hint}"
        return enriched


def make_disclaimer(profile: AnonymousProfile) -> str:
    return profile.disclaimer_template
