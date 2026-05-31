"""Human-readable explanation of a candidate's match score."""


def score_tier(score: float) -> str:
    if score >= 75:
        return "Strong match"
    if score >= 50:
        return "Moderate match"
    if score >= 25:
        return "Weak match"
    return "Poor match"


def build_explanation(
    score: float,
    similarity: float,
    matched: set[str],
    missing: set[str],
    experience_years: float,
) -> str:
    """Compose a plain-English rationale from the scoring signals."""
    parts = [f"{score_tier(score)} ({round(score)}/100)."]

    if similarity >= 0.6:
        parts.append("Resume content is highly relevant to the role.")
    elif similarity >= 0.35:
        parts.append("Resume content is somewhat relevant to the role.")
    else:
        parts.append("Resume content has low semantic relevance to the role.")

    total = len(matched) + len(missing)
    if total == 0:
        parts.append("No specific skills were identified in the job description.")
    elif not missing:
        parts.append(
            f"All {total} required skills are present "
            f"({', '.join(sorted(matched))})."
        )
    elif not matched:
        parts.append(
            f"None of the {total} required skills were found; "
            f"missing {', '.join(sorted(missing))}."
        )
    else:
        parts.append(
            f"{len(matched)} of {total} required skills present; "
            f"missing {', '.join(sorted(missing))}."
        )

    if experience_years > 0:
        parts.append(f"{int(experience_years)} years of experience detected.")
    else:
        parts.append("No explicit years of experience detected.")

    return " ".join(parts)
