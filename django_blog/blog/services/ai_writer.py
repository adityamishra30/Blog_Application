import json
import re
from urllib import error, request

from django.conf import settings


class AIServiceError(Exception):
    pass


_DISALLOWED_TOPIC_PATTERNS = [
    r"\b(bomb|explosive|weapon|firearm)\b",
    r"\b(hate speech|racial slur|terrorist)\b",
    r"\b(phishing|malware|ransomware|ddos)\b",
    r"\b(sexually explicit|porn)\b",
]

_DISALLOWED_OUTPUT_PATTERNS = [
    r"\b(build a bomb|make a bomb)\b",
    r"\b(credit card fraud|identity theft)\b",
    r"\b(hate campaign|ethnic cleansing)\b",
]


def _build_prompt(topic):
    return (
        "You are an editorial writing assistant for a public blogging platform. "
        "Write a concise, informative, and engaging article that is safe for a general audience. "
        "Do not include instructions for violence, self-harm, hate, illegal acts, explicit sexual content, "
        "or targeted harassment. Return ONLY valid JSON with keys title and content.\n\n"
        f"Topic: {topic}"
    )


def _contains_pattern(text, patterns):
    lowered = (text or "").lower()
    return any(re.search(pattern, lowered) for pattern in patterns)


def _extract_json_object(raw_text):
    cleaned = (raw_text or "").strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned)
        cleaned = re.sub(r"\n?```$", "", cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if not match:
            raise AIServiceError("AI response was not in the expected format.")
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError as exc:
            raise AIServiceError("AI response could not be parsed.") from exc


def generate_article_from_topic(topic):
    topic = (topic or "").strip()

    if not topic:
        raise AIServiceError("Topic is required.")
    if len(topic) < 3 or len(topic) > 120:
        raise AIServiceError("Topic must be between 3 and 120 characters.")
    if _contains_pattern(topic, _DISALLOWED_TOPIC_PATTERNS):
        raise AIServiceError("The provided topic is not allowed.")

    api_key = settings.AI_GENERATION_API_KEY
    if not api_key:
        raise AIServiceError("AI generation is not configured yet.")

    payload = {
        "model": settings.AI_GENERATION_MODEL,
        "temperature": 0.7,
        "max_tokens": settings.AI_GENERATION_MAX_TOKENS,
        "messages": [
            {"role": "system", "content": "Return strict JSON only."},
            {"role": "user", "content": _build_prompt(topic)},
        ],
    }

    req = request.Request(
        settings.AI_GENERATION_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"******",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=settings.AI_GENERATION_TIMEOUT_SECONDS) as response:
            data = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        raise AIServiceError(f"AI provider error: {exc.code}") from exc
    except error.URLError as exc:
        raise AIServiceError("Could not reach AI provider.") from exc
    except TimeoutError as exc:
        raise AIServiceError("AI generation timed out.") from exc
    except json.JSONDecodeError as exc:
        raise AIServiceError("Invalid AI provider response.") from exc

    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise AIServiceError("AI provider response is missing content.") from exc

    parsed = _extract_json_object(content)
    title = (parsed.get("title") or "").strip()
    article_content = (parsed.get("content") or "").strip()

    if not title or not article_content:
        raise AIServiceError("AI response did not include a title and content.")
    if _contains_pattern(f"{title}\n{article_content}", _DISALLOWED_OUTPUT_PATTERNS):
        raise AIServiceError("Generated content did not pass safety checks.")

    return {
        "title": title[:200],
        "content": article_content[:10000],
        "topic": topic,
    }
