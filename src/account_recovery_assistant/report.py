from typing import Any


def render_markdown(plan: dict[str, Any]) -> str:
    if not plan.get("allowed", False):
        return "\n".join(
            [
                "# Account Recovery Plan",
                "",
                "## Safety Refusal",
                "",
                str(plan.get("reason", "This request is not supported.")),
                "",
            ]
        )

    lines = [
        "# Account Recovery Plan",
        "",
        f"Service: {plan['service']}",
        f"Case type: {plan['case_type']}",
        f"Incident: {plan.get('incident_title') or 'General recovery case'}",
        "",
        "## Next Best Action",
        "",
        plan["next_best_action"],
        "",
        "## Prepare Now",
        "",
        *_bullet_list(plan["prepare_now"]),
        "",
        "## What Can Make This Worse",
        "",
        *_bullet_list(plan["what_can_make_this_worse"]),
        "",
        "## Escalate When",
        "",
        *_bullet_list(plan["escalate_when"]),
        "",
        f"Expected timeline: {plan['expected_timeline']}",
        "",
        "## Checklist",
        "",
        *_bullet_list(plan["checklist"]),
        "",
        "## Evidence To Prepare",
        "",
        *_bullet_list(plan["evidence"]),
        "",
        "## Official Links",
        "",
        *_link_list(plan["official_links"]),
        "",
        "## Knowledge Freshness",
        "",
        f"- Last verified: {plan['knowledge_base']['last_verified_at'] or 'Unknown'}",
        f"- Review due: {plan['knowledge_base']['review_due_at'] or 'Unknown'}",
        f"- Review cadence: {plan['knowledge_base']['review_cadence_days'] or 'Unknown'} days",
        f"- Confidence: {plan['knowledge_base']['confidence']}",
        f"- Status: {plan['knowledge_base']['status']}",
        f"- Stale: {'yes' if plan['knowledge_base']['stale'] else 'no'}",
        "",
        "## Common Mistakes To Avoid",
        "",
        *_bullet_list(plan["common_mistakes"]),
        "",
        "## Support Message",
        "",
        plan["support_message"],
        "",
        "## Source Notes",
        "",
        *_bullet_list(plan["source_notes"]),
        "",
        "## Post-Recovery Hardening",
        "",
        *_bullet_list(plan["hardening_steps"]),
        "",
        "## Safety Warnings",
        "",
        *_bullet_list(plan["safety_warnings"]),
        "",
    ]
    return "\n".join(lines)


def _bullet_list(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items]


def _link_list(items: list[dict[str, str]]) -> list[str]:
    return [f"- [{item['label']}]({item['url']})" for item in items]
