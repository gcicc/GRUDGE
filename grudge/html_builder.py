"""Raw HTML generation — Times New Roman, blue links, 1997 aesthetic."""

import random
from datetime import datetime, timezone


def _time_ago(published: datetime) -> str:
    """Human-readable time ago string."""
    now = datetime.now(timezone.utc)
    delta = now - published
    minutes = int(delta.total_seconds() / 60)
    if minutes < 1:
        return "just now"
    if minutes < 60:
        return f"{minutes}m ago"
    hours = minutes // 60
    if hours < 24:
        return f"{hours}h ago"
    days = hours // 24
    return f"{days}d ago"


def _traffic_counter() -> str:
    """Fake traffic counter that looks impressive."""
    count = random.randint(8_000_000, 45_000_000)
    return f"{count:,}"


def _render_top_story(h: dict) -> list[str]:
    """Render the dominant top story."""
    prefix = "\U0001f6a8 " if h.get("breaking") else ""
    return [
        '<div style="text-align: center; padding: 10px 0;">',
        f'<h2 style="font-size: 1.8em; margin: 5px 0;">'
        f'<a href="{h["link"]}" style="color: #cc0000; text-decoration: none;">'
        f'{prefix}{h["title"]}</a></h2>',
        f'<p style="font-size: 0.85em; color: #555;">{h["source"]} | {_time_ago(h["published"])}</p>',
        "</div>",
        "<hr>",
    ]


def _render_headline(h: dict) -> list[str]:
    """Render a single headline row."""
    prefix = "\U0001f6a8 " if h.get("breaking") else ""
    return [
        "<p>",
        f'<a href="{h["link"]}" style="color: blue; text-decoration: underline;">'
        f"<b>{prefix}{h['title']}</b></a>",
        f'<br><small style="color: #666;">{h["source"]} | {_time_ago(h["published"])}</small>',
        "</p>",
    ]


def _render_tech_item(h: dict) -> list[str]:
    """Render a tech/AI item with TL;DR style summary."""
    return [
        '<div style="margin-bottom: 12px;">',
        f'<a href="{h["link"]}" style="color: blue; text-decoration: underline;">'
        f"<b>{h['title']}</b></a>",
        f'<br><small style="color: #666;">{h["source"]} | {_time_ago(h["published"])}</small>',
        "</div>",
    ]


def _render_portfolio_item(h: dict) -> list[str]:
    """Render a portfolio news item with ticker badge."""
    ticker = h.get("source", "")
    return [
        '<div style="margin-bottom: 12px;">',
        f'<span style="background-color: #006400; color: white; padding: 1px 6px; '
        f'font-size: 0.8em; font-weight: bold;">{ticker}</span> ',
        f'<a href="{h["link"]}" style="color: blue; text-decoration: underline;">'
        f"<b>{h['title']}</b></a>",
        f'<br><small style="color: #666;">{_time_ago(h["published"])}</small>',
        "</div>",
    ]


def build_page(
    news: list[dict],
    tech: list[dict] | None = None,
    portfolio: list[dict] | None = None,
) -> str:
    """Generate the full HTML page with news + optional tech + portfolio sections."""
    now = datetime.now(timezone.utc).strftime("%A, %B %d, %Y %H:%M UTC")

    lines = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>GRUDGE REPORT</title>",
        "</head>",
        '<body style="font-family: \'Times New Roman\', Times, serif; '
        'max-width: 640px; margin: 0 auto; padding: 10px; '
        'background-color: #ffffff;">',
        "",
        '<div style="text-align: center;">',
        '<h1 style="font-size: 2.5em; margin-bottom: 0; letter-spacing: 2px;">GRUDGE REPORT</h1>',
        f'<p style="font-size: 0.9em; color: #333;">{now}</p>',
        f'<p style="font-size: 0.8em; color: #666;">{_traffic_counter()} VISITS THIS MONTH</p>',
        "</div>",
        "<hr>",
    ]

    # === NEWS SECTION ===
    if not news:
        lines.append("<p><b>NO HEADLINES AVAILABLE. THE MEDIA IS HIDING SOMETHING.</b></p>")
        lines.append("<hr>")
    else:
        lines.extend(_render_top_story(news[0]))
        for h in news[1:]:
            lines.extend(_render_headline(h))
        lines.append("<hr>")

    # === TECH & AI SECTION ===
    if tech:
        lines.extend([
            "",
            '<div style="text-align: center; padding: 10px 0; background-color: #f0f0f0;">',
            '<h2 style="font-size: 1.4em; margin: 5px 0; letter-spacing: 1px;">'
            "TL;DR &mdash; TECH &amp; AI</h2>",
            '<p style="font-size: 0.8em; color: #555;">What the machines are up to</p>',
            "</div>",
            "<hr>",
        ])
        for h in tech:
            lines.extend(_render_tech_item(h))
        lines.append("<hr>")

    # === PORTFOLIO SECTION ===
    if portfolio:
        lines.extend([
            "",
            '<div style="text-align: center; padding: 10px 0; background-color: #e8f5e9;">',
            '<h2 style="font-size: 1.4em; margin: 5px 0; letter-spacing: 1px;">'
            "MY PORTFOLIO &mdash; NEWS</h2>",
            '<p style="font-size: 0.8em; color: #555;">What your money is doing</p>',
            "</div>",
            "<hr>",
        ])
        for h in portfolio:
            lines.extend(_render_portfolio_item(h))
        lines.append("<hr>")

    # Footer
    lines.extend([
        '<p style="text-align: center; font-size: 0.75em; color: #999;">',
        "GRUDGE REPORT &copy; 2025. All links property of their respective owners.",
        "<br>Aggregated by robots. Read by patriots.",
        "</p>",
        "</body>",
        "</html>",
    ])

    return "\n".join(lines)
