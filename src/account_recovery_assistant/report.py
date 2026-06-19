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
        "## Support Message",
        "",
        plan["support_message"],
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
