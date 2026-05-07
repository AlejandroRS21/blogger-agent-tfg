"""
Style Extractor Agent.

Analyza el corpus de un blogger para extraer:
- Vocabulario y expresiones características
- Patrones de transición
- Topics y temas que trata
- Estructura de los artículos
- Tono y voz

Este agente analiza el corpus real para crear un perfil de estilo preciso.
"""

import json
import re
from typing import List, Dict, Any, Optional
from collections import Counter
from dataclasses import dataclass, asdict


@dataclass
class StyleProfile:
    """Perfil de estilo extraído del blogger."""

    alias: str
    vocabulary: List[str]
    expressions: List[str]
    transition_phrases: List[str]
    topics: List[str]
    tone: str
    voice: str
    sentence_pattern: str
    paragraph_pattern: str
    common_opens: List[str]
    common_closes: List[str]
    use_of_humor: str
    technical_level: str
    engagement_style: str


class StyleExtractor:
    """Extrae el estilo de escritura de un blogger a partir de su corpus."""

    def __init__(self, corpus_file: str = None):
        self.corpus_file = corpus_file
        self.corpus = None
        self.stopwords = self._get_spanish_stopwords()

    def load_corpus(self, filepath: str) -> List[Dict]:
        """Carga el corpus desde un archivo JSON."""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.corpus = data["posts"]
        return self.corpus

    def extract_profile(self, corpus_file: str = None, alias: str = "JaviPas") -> StyleProfile:
        """Extrae un perfil de estilo completo del corpus."""
        if corpus_file:
            self.load_corpus(corpus_file)

        if not self.corpus:
            raise ValueError("No corpus loaded. Provide corpus_file path.")

        all_text = " ".join([p["content"] for p in self.corpus])

        vocabulary = self._extract_vocabulary(all_text)
        expressions = self._extract_expressions(all_text)
        transitions = self._extract_transitions(all_text)
        topics = self._extract_topics(all_text)
        tone, voice = self._analyze_tone_and_voice(all_text)
        sentence_pattern = self._analyze_sentences(all_text)
        paragraph_pattern = self._analyze_paragraphs(all_text)
        common_opens = self._extract_opening_patterns()
        common_closes = self._extract_closing_patterns()
        use_of_humor = self._analyze_humor(all_text)
        technical_level = self._analyze_technical_level(all_text)
        engagement_style = self._analyze_engagement(all_text)

        return StyleProfile(
            alias=alias,
            vocabulary=vocabulary,
            expressions=expressions,
            transition_phrases=transitions,
            topics=topics,
            tone=tone,
            voice=voice,
            sentence_pattern=sentence_pattern,
            paragraph_pattern=paragraph_pattern,
            common_opens=common_opens,
            common_closes=common_closes,
            use_of_humor=use_of_humor,
            technical_level=technical_level,
            engagement_style=engagement_style,
        )

    def _get_spanish_stopwords(self) -> set:
        return {
            "de",
            "la",
            "que",
            "el",
            "en",
            "y",
            "a",
            "los",
            "del",
            "se",
            "las",
            "por",
            "un",
            "para",
            "con",
            "no",
            "una",
            "su",
            "al",
            "lo",
            "como",
            "más",
            "pero",
            "sus",
            "le",
            "ya",
            "o",
            "este",
            "sí",
            "porque",
            "esta",
            "entre",
            "cuando",
            "muy",
            "sin",
            "sobre",
            "también",
            "me",
            "hasta",
            "hay",
            "donde",
            "han",
            "quien",
            "están",
            "estado",
            "desde",
            "todo",
            "nos",
            "durante",
            "todos",
            "uno",
            "les",
            "ni",
            "contra",
            "otros",
            "ese",
            "eso",
            "ante",
            "ellos",
            "e",
            "esto",
            "mí",
            "antes",
            "algunos",
            "qué",
            "unos",
            "yo",
            "otro",
            "otras",
            "otra",
            "él",
            "tanto",
            "esa",
            "estos",
            "mucho",
            "quienes",
            "nada",
            "muchos",
            "cual",
            "poco",
            "ella",
            "estar",
            "estas",
            "algunas",
            "algo",
            "nosotros",
            "mi",
            "mis",
            "tú",
            "te",
            "ti",
            "tu",
            "tus",
            "ellas",
            "nosotras",
            "vosotros",
            "vosotras",
            "os",
            "he",
            "has",
            "ha",
            "hemos",
            "habéis",
            "han",
            "soy",
            "eres",
            "es",
            "somos",
            "sois",
            "son",
            "sea",
            "seas",
            "seamos",
            "seáis",
            "sean",
            "era",
            "eras",
            "éramos",
            "erais",
            "eran",
            "fui",
            "fuiste",
            "fue",
            "fuimos",
            "fuisteis",
            "fueron",
            "tengo",
            "tienes",
            "tiene",
            "tenemos",
            "tenéis",
            "tienen",
            "ser",
            "estar",
            "hacer",
            "poder",
            "decir",
            "ver",
            "dar",
            "saber",
            "querer",
            "llegar",
            "pasar",
            "deber",
            "poner",
            "parecer",
            "quedar",
            "creer",
            "sacar",
            "salir",
            "conocer",
            "dejar",
            "pensar",
            "entender",
            "buscar",
            "existir",
            "esperar",
            "trabajar",
            "vivir",
            "sentir",
            "conseguir",
            "entrar",
            "aparecer",
            "producir",
            "continuar",
            "servir",
            "empezar",
            "incluir",
            "leer",
            "mantener",
            "escribir",
            "permitir",
            "indicar",
            "conducir",
        }

    def _extract_vocabulary(self, text: str, top_n: int = 100) -> List[str]:
        words = re.findall(r"\b[a-záéíóúñü]+\b", text.lower())
        filtered = [w for w in words if w not in self.stopwords and len(w) > 3]
        counter = Counter(filtered)
        return [word for word, count in counter.most_common(top_n)]

    def _extract_expressions(self, text: str) -> List[str]:
        candidate_expressions = [
            "me alucina",
            "flipar",
            "mazo",
            "brutal",
            "dicho y hecho",
            "el caso es que",
            "total que",
            "ciertamente",
            "como digo",
            "insisto",
            "no era para tanto",
            "no es para tanto",
            "vaya tela",
            "a ver",
            "toma ya",
            "que te voy a contar",
            "si es que",
            "por lo visto",
            "al final",
            "mala idea",
            "buena idea",
            "me he comprado",
            "he usado",
            "probando",
            "feliz",
            "ahora resulta que",
            "vaya sorpresa",
            "para variar",
            "en serio",
            "de verdad",
            "a decir verdad",
            "o sea",
            "vamos a ver",
            "mira tú",
            "fíjate",
            "y tal",
            "por cierto",
            "a todo esto",
            "mientras tanto",
            "al grano",
            "para qué contar",
            "ya sabes",
            "ni que decir tiene",
            "cabría añadir",
            "cabe destacar",
        ]

        found = []
        text_lower = text.lower()
        for expr in candidate_expressions:
            if expr in text_lower:
                found.append(expr)

        return found

    def _extract_transitions(self, text: str) -> List[str]:
        transition_patterns = [
            "por otro lado",
            "sin embargo",
            "a continuación",
            "por tanto",
            "en consecuencia",
            "así mismo",
            "del mismo modo",
            "por otra parte",
            "en primer lugar",
            "en segundo lugar",
            "por último",
            "en cuanto a",
            "respecto a",
            "en relación con",
            "esto significa",
            "esto implica",
            "al mismo tiempo",
            "mientras tanto",
            "aun así",
            "a pesar de",
            "no obstante",
            "con todo",
            "en cualquier caso",
            "en todo caso",
        ]

        found = []
        text_lower = text.lower()
        for trans in transition_patterns:
            if trans in text_lower:
                found.append(trans)

        return found

    def _extract_topics(self, text: str) -> List[str]:
        text_lower = text.lower()

        topics = {
            "Inteligencia Artificial": [
                "ia",
                "inteligencia artificial",
                "ai",
                "chatgpt",
                "claude",
                "gemini",
                "gpt",
                "llm",
                "machine learning",
            ],
            "Apple": [
                "apple",
                "macbook",
                "iphone",
                "ipad",
                "ios",
                "macos",
                "apple watch",
                "airpods",
            ],
            "Microsoft": ["microsoft", "windows", "office", "azure", "copilot", "xbox"],
            "Google": ["google", "android", "pixel", "chrome", "gmail", "youtube"],
            "Tecnología": ["tecnología", "tech", "gadget", "hardware", "software"],
            "Opinión": ["opinión", "review", "análisis", "reflexión"],
            "Movilidad": ["coche", "tesla", "vehículo", "eléctrico"],
            "Cine/Series": ["serie", "película", "cine", "netflix"],
            "Personal": ["familia", "niños", "casa", "vida personal"],
        }

        found_topics = []
        for topic, keywords in topics.items():
            count = sum(text_lower.count(kw) for kw in keywords)
            if count > 3:
                found_topics.append(topic)

        return found_topics

    def _analyze_tone_and_voice(self, text: str) -> tuple:
        text_lower = text.lower()

        informal_words = ["mazo", "brutal", "flipar", "alucina", "toma ya", "vaya tela"]
        informal_count = sum(1 for w in informal_words if w in text_lower)

        if informal_count > 3:
            tone = "coloquial, conversacional, cercano, con humor"
        else:
            tone = "formal con toques coloquiales"

        first_person = text_lower.count("yo ") + text_lower.count("me ") + text_lower.count("mi ")

        if first_person > 50:
            voice = "primera persona, cercano al lector, narrativo"
        else:
            voice = "primera persona ocasional"

        return tone, voice

    def _analyze_sentences(self, text: str) -> str:
        sentences = re.split(r"[.!?]+", text)
        lengths = [len(s.split()) for s in sentences if s.strip()]

        if not lengths:
            return "medium"

        avg = sum(lengths) / len(lengths)

        if avg < 12:
            return "oraciones cortas y directas"
        elif avg < 18:
            return "oraciones de longitud media, fluidas"
        else:
            return "oraciones largas y elaboradas"

    def _analyze_paragraphs(self, text: str) -> str:
        paragraphs = text.split("\n\n")
        lengths = [len(p.split()) for p in paragraphs if p.strip()]

        if not lengths:
            return "medium"

        avg = sum(lengths) / len(lengths)

        if avg < 30:
            return "párrafos cortos (2-4 oraciones)"
        elif avg < 60:
            return "párrafos de longitud media (4-6 oraciones)"
        else:
            return "párrafos extensos (6+ oraciones)"

    def _extract_opening_patterns(self) -> List[str]:
        if not self.corpus:
            return []

        openings = []
        for post in self.corpus[:10]:
            content = post["content"].strip()
            first_sentence = content.split(".")[0][:100] if content else ""
            if first_sentence:
                openings.append(first_sentence)

        return openings[:5]

    def _extract_closing_patterns(self) -> List[str]:
        if not self.corpus:
            return []

        closings = []
        for post in self.corpus[:10]:
            content = post["content"].strip()
            sentences = re.split(r"[.!?]+", content)
            last = sentences[-2].strip() if len(sentences) > 1 else ""
            if last:
                closings.append(last[:100])

        return closings[:5]

    def _analyze_humor(self, text: str) -> str:
        text_lower = text.lower()

        humor_markers = ["jeje", "jaja", "flipar", "alucina", "vaya tela", "toma ya"]
        irony_markers = ["vaya", "resulta que", "para variar", "como no"]

        humor_count = sum(1 for m in humor_markers if m in text_lower)
        irony_count = sum(1 for m in irony_markers if m in text_lower)

        if humor_count > 5:
            return "humorístico, usa expresiones coloquiales coloquiales"
        elif irony_count > 3:
            return "humor irónico y auto-deprecativo"
        else:
            return "tono semiformal con toques de humor"

    def _analyze_technical_level(self, text: str) -> str:
        text_lower = text.lower()

        tech_terms = [
            "api",
            "sdk",
            "framework",
            "backend",
            "frontend",
            "cloud",
            "ia",
            "machine learning",
            "linux",
        ]
        tech_count = sum(text_lower.count(t) for t in tech_terms)

        if tech_count > 20:
            return "técnico-avanzado"
        elif tech_count > 10:
            return "técnico-intermedio, explica conceptos de forma accesible"
        else:
            return "accesible, evita tecnicismos excesivos"

    def _analyze_engagement(self, text: str) -> str:
        text_lower = text.lower()

        engagement_markers = [
            "qué opinas",
            "qué te parece",
            "comenta",
            "suscríbete",
            "gracias por leer",
        ]
        count = sum(1 for m in engagement_markers if m in text_lower)

        if count > 3:
            return "alta interacción, invita a comentar y compartir"
        else:
            return "interacción moderada"

    def to_prompt_context(self, profile: StyleProfile) -> str:
        context = f"""
ESTILO DEL BLOGGER: {profile.alias}
=====================================

Tono: {profile.tone}
Voz: {profile.voice}

VOCABULARIO CARACTERÍSTICO (usa estas palabras):
{", ".join(profile.vocabulary[:30])}

EXPRESIONES TÍPICAS (incorpáralas naturalmente):
{", ".join(profile.expressions)}

FRASES DE TRANSICIÓN (úsalas para conectar ideas):
{", ".join(profile.transition_phrases[:10])}

TEMAS QUE TRATA:
{", ".join(profile.topics)}

PATRÓN DE ORACIONES: {profile.sentence_pattern}
PATRÓN DE PÁRRAFOS: {profile.paragraph_pattern}
USO DEL HUMOR: {profile.use_of_humor}
NIVEL TÉCNICO: {profile.technical_level}
INTERACCIÓN CON LECTORES: {profile.engagement_style}

EJEMPLO DE CÓMO EMPIEZA SUS ARTÍCULOS:
{profile.common_opens[0] if profile.common_opens else "N/A"}

EJEMPLO DE CÓMO TERMINA SUS ARTÍCULOS:
{profile.common_closes[0] if profile.common_closes else "N/A"}
"""
        return context

    def save_profile(self, profile: StyleProfile, filepath: str):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(asdict(profile), f, ensure_ascii=False, indent=2)

    def load_profile(self, filepath: str) -> StyleProfile:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return StyleProfile(**data)


if __name__ == "__main__":
    extractor = StyleExtractor()
    profile = extractor.extract_profile("javipas_corpus.json", "JaviPas")

    print("=== PERFIL DE ESTILO EXTRAÍDO ===")
    print(f"Alias: {profile.alias}")
    print(f"Tono: {profile.tone}")
    print(f"Voz: {profile.voice}")
    print(f"Expresiones: {profile.expressions}")
    print(f"Temas: {profile.topics}")
    print(f"Vocabulario top 20: {profile.vocabulary[:20]}")

    extractor.save_profile(profile, "javipas_style_profile.json")
    print("\n✓ Perfil guardado en javipas_style_profile.json")

    context = extractor.to_prompt_context(profile)
    with open("javipas_prompt_context.txt", "w", encoding="utf-8") as f:
        f.write(context)
    print("✓ Contexto guardado en javipas_prompt_context.txt")
