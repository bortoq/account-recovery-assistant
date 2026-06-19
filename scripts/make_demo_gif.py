from __future__ import annotations

import sys
from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from account_recovery_assistant import generate_recovery_plan  # noqa: E402

WIDTH = 1280
HEIGHT = 820
BG = "#f6efe4"
PANEL = "#fffaf3"
INK = "#1e1d1a"
MUTED = "#6c655d"
ACCENT = "#165d52"
ACCENT_SOFT = "#d8ede8"
WARNING_BG = "#fde8da"
WARNING = "#8a3f16"
BORDER = "#d9cbbb"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


H1 = font(44, bold=True)
H2 = font(30, bold=True)
BODY = font(22)
SMALL = font(18)
BADGE = font(16, bold=True)


def new_canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((40, 28, WIDTH - 40, HEIGHT - 28), radius=32, fill=PANEL, outline=BORDER, width=2)
    return image, draw


def text_block(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, width: int, *, fnt, fill=INK, line_gap=10) -> int:
    x, y = xy
    max_chars = max(12, int(width / max(10, fnt.size * 0.58)))
    lines: list[str] = []
    for part in text.splitlines() or [""]:
        if not part:
            lines.append("")
            continue
        lines.extend(wrap(part, width=max_chars))
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap
    return y


def pill(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, *, fill=ACCENT_SOFT, text_fill=ACCENT) -> None:
    draw.rounded_rectangle(box, radius=999, fill=fill, outline=None)
    bbox = draw.textbbox((0, 0), text, font=BADGE)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x1, y1, x2, y2 = box
    draw.text((x1 + (x2 - x1 - tw) / 2, y1 + (y2 - y1 - th) / 2 - 1), text, font=BADGE, fill=text_fill)


def draw_header(draw: ImageDraw.ImageDraw, subtitle: str) -> None:
    pill(draw, (90, 72, 250, 108), "Safety-first recovery")
    draw.text((90, 126), "Account Recovery Wizard", font=H1, fill=INK)
    draw.text((90, 184), subtitle, font=BODY, fill=MUTED)


def card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, body: str, *, accent=False) -> None:
    fill = "#fffdf8" if not accent else "#f7fbfa"
    outline = ACCENT if accent else BORDER
    draw.rounded_rectangle(box, radius=24, fill=fill, outline=outline, width=2)
    x1, y1, x2, _ = box
    draw.text((x1 + 24, y1 + 20), title, font=H2, fill=INK)
    text_block(draw, (x1 + 24, y1 + 64), body, x2 - x1 - 48, fnt=BODY, fill=MUTED, line_gap=8)


def checklist_panel(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, items: list[str], *, warning=False) -> None:
    fill = WARNING_BG if warning else "#fffdf8"
    outline = "#f0b893" if warning else BORDER
    text_fill = WARNING if warning else INK
    draw.rounded_rectangle(box, radius=20, fill=fill, outline=outline, width=2)
    x1, y1, x2, _ = box
    draw.text((x1 + 20, y1 + 18), title, font=H2, fill=text_fill)
    y = y1 + 64
    for item in items[:4]:
        draw.ellipse((x1 + 22, y + 10, x1 + 34, y + 22), fill=ACCENT if not warning else WARNING)
        y = text_block(draw, (x1 + 46, y), item, x2 - x1 - 66, fnt=SMALL, fill=text_fill if warning else MUTED, line_gap=6) + 6


def frame_incident_picker() -> Image.Image:
    image, draw = new_canvas()
    draw_header(draw, "Choose the incident that best matches the recovery problem and get a guided plan.")
    card(draw, (90, 250, 600, 420), "Lost MFA device for Google", "Backup codes, trusted session checks, and Google recovery context.", accent=True)
    card(draw, (640, 250, 1150, 420), "Apple trusted-device loss", "Trusted device, trusted phone, and account recovery wait period.")
    card(draw, (90, 450, 600, 620), "Meta account hacked", "Instagram/Facebook takeover, identity review, and business asset risk.")
    card(draw, (640, 450, 1150, 620), "Microsoft admin lockout", "Backup admin, tenant proof, and business support escalation.")
    draw.text((92, 692), "Step 1 of 3", font=SMALL, fill=MUTED)
    pill(draw, (190, 680, 356, 716), "Pick your incident")
    return image


def frame_questionnaire() -> Image.Image:
    image, draw = new_canvas()
    draw_header(draw, "Answer a short normalized questionnaire. The same contract drives CLI and web flows.")
    draw.text((90, 250), "Lost MFA device for a Google account", font=H2, fill=INK)
    questions = [
        ("Role", "Rightful owner"),
        ("Still know the password?", "Yes"),
        ("Have backup codes?", "No"),
        ("Control recovery email?", "Yes"),
        ("Trusted signed-in device?", "No"),
    ]
    y = 304
    for label, answer in questions:
        draw.rounded_rectangle((90, y, 1150, y + 72), radius=18, fill="#fffdf8", outline=BORDER, width=2)
        draw.text((112, y + 18), label, font=BODY, fill=INK)
        pill(draw, (850, y + 16, 1120, y + 52), answer, fill=ACCENT_SOFT, text_fill=ACCENT)
        y += 88
    draw.text((92, 744), "Step 2 of 3", font=SMALL, fill=MUTED)
    pill(draw, (190, 732, 428, 768), "Answer the questionnaire")
    return image


def frame_google_plan() -> Image.Image:
    plan = generate_recovery_plan(
        {
            "service": "Google",
            "incident_id": "gmail_mfa_loss",
            "lost_factor": "authenticator_app",
            "still_knows_password": True,
            "has_backup_codes": False,
            "has_recovery_email": True,
            "has_trusted_device": False,
            "role": "owner",
        }
    )
    image, draw = new_canvas()
    draw_header(draw, "Get a real plan with a next-best action, evidence prep, and escalation triggers.")
    checklist_panel(draw, (90, 250, 1190, 380), "Next Best Action", [plan["next_best_action"]])
    checklist_panel(draw, (90, 408, 610, 730), "Prepare Now", plan["prepare_now"])
    checklist_panel(draw, (670, 408, 1190, 730), "Escalate When", plan["escalate_when"])
    draw.text((92, 748), f"Decision path: {plan['decision_path_id']}", font=SMALL, fill=MUTED)
    return image


def frame_meta_warning() -> Image.Image:
    plan = generate_recovery_plan(
        {
            "service": "Instagram",
            "incident_id": "meta_account_hacked",
            "account_state": "locked_suspicious_activity",
            "still_controls_email": False,
            "still_controls_phone": True,
            "has_photo_id": True,
            "business_account": True,
            "role": "owner",
        }
    )
    image, draw = new_canvas()
    draw_header(draw, "The wizard also surfaces freshness warnings and business-asset risk where recovery quality is less certain.")
    checklist_panel(
        draw,
        (90, 248, 1190, 376),
        "Needs Review Warning",
        [
            "This Meta incident record is marked needs_review.",
            "Re-check the official flow before relying on service-specific details.",
        ],
        warning=True,
    )
    checklist_panel(draw, (90, 392, 610, 730), "Prepare Now", plan["prepare_now"])
    checklist_panel(draw, (670, 392, 1190, 730), "What Can Make This Worse", plan["what_can_make_this_worse"])
    draw.text((92, 748), f"Decision path: {plan['decision_path_id']}", font=SMALL, fill=MUTED)
    return image


def main() -> None:
    out_dir = ROOT / "docs" / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    frames = [
        frame_incident_picker(),
        frame_questionnaire(),
        frame_google_plan(),
        frame_meta_warning(),
    ]
    gif_path = out_dir / "demo.gif"
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=[4200, 4200, 5100, 5400],
        loop=0,
        optimize=True,
    )
    frames[0].save(out_dir / "demo-poster.png")
    print(gif_path)


if __name__ == "__main__":
    main()
