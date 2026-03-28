"""Raw HTML generation — Times New Roman, blue links, 3-column Drudge layout."""

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


def _link(h: dict, color: str = "blue") -> str:
    """Render a single headline link."""
    prefix = "\U0001f6a8 " if h.get("breaking") else ""
    return (
        f'<a href="{h["link"]}" style="color: {color};">'
        f"{prefix}{h['title']}</a>"
    )


def _headline_block(h: dict) -> str:
    """A headline with source line underneath."""
    return (
        f"<b>{_link(h)}</b>"
        f'<br><font size="1" color="#666666">{h["source"]} | {_time_ago(h["published"])}</font>'
        f"<br><br>"
    )


def _portfolio_block(h: dict) -> str:
    """Portfolio headline with ticker badge."""
    ticker = h.get("source", "")
    return (
        f'<font style="background-color: #006400; color: white; padding: 1px 5px; '
        f'font-size: 10px;"><b>{ticker}</b></font> '
        f'{_link(h)}'
        f'<br><font size="1" color="#666666">{_time_ago(h["published"])}</font>'
        f"<br><br>"
    )


def _split_list(items: list, n: int) -> list[list]:
    """Split a list into n roughly equal parts."""
    k, m = divmod(len(items), n)
    return [items[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]


def build_page(
    news: list[dict],
    tech: list[dict] | None = None,
    portfolio: list[dict] | None = None,
    weather: list[dict] | None = None,
) -> str:
    """Generate the full HTML page in 3-column Drudge Report layout."""
    now = datetime.now(timezone.utc).strftime("%A, %B %d, %Y %H:%M UTC")

    # Col 1: All news, Col 2: All tech, Col 3: All portfolio
    top_story = news[0] if news else None
    remaining_news = news[1:] if news else []

    lines = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>GRUDGE REPORT</title>",
        "</head>",
        '<body style="font-family: \'Times New Roman\', Times, serif; '
        "margin: 0; padding: 0; background-color: #ffffff;\">",
    ]

    # WEATHER BANNER
    if weather:
        weather_parts = " &nbsp;&bull;&nbsp; ".join(
            f"<b>{w['name']}:</b> {w['weather']}" for w in weather
        )
        lines.extend([
            "",
            '<div style="background-color: #1a1a2e; color: #e0e0e0; text-align: center; '
            'padding: 4px 10px; font-size: 12px;">',
            weather_parts,
            "</div>",
        ])

    lines.extend([
        "",
        "<!-- HEADER -->",
        '<div style="text-align: center; padding: 10px 0;">',
        '<h1 style="font-size: 2.8em; margin: 0; letter-spacing: 3px;">GRUDGE REPORT</h1>',
        f'<font size="2" color="#333333">{now}</font>',
        "</div>",
        "<hr>",
    ])

    # TOP STORY — full width banner
    if top_story:
        prefix = "\U0001f6a8 " if top_story.get("breaking") else ""
        lines.extend([
            '<div style="text-align: center; padding: 8px 20px;">',
            f'<font size="5"><b>'
            f'<a href="{top_story["link"]}" style="color: #cc0000; text-decoration: none;">'
            f'{prefix}{top_story["title"]}</a></b></font>',
            f'<br><font size="1" color="#555555">'
            f'{top_story["source"]} | {_time_ago(top_story["published"])}</font>',
            "</div>",
            "<hr>",
        ])

    # 3-COLUMN LAYOUT via table (Drudge style — no CSS grid, just raw tables)
    lines.extend([
        "",
        '<table width="100%" cellpadding="8" cellspacing="0" border="0">',
        "<tr valign=\"top\">",
        "",
        "<!-- LEFT COLUMN: US & WORLD NEWS -->",
        '<td width="33%" style="border-right: 1px solid #cccccc; padding: 8px; font-size: 14px;">',
        '<div style="text-align: center; padding: 4px 0; background-color: #f0f0f0;">',
        '<font size="3"><b>US &amp; WORLD NEWS</b></font>',
        "</div>",
        "<hr>",
    ])

    if not remaining_news:
        lines.append("<b>NO HEADLINES AVAILABLE. THE MEDIA IS HIDING SOMETHING.</b>")
    else:
        for h in remaining_news:
            lines.append(_headline_block(h))

    lines.extend([
        "</td>",
        "",
        "<!-- CENTER COLUMN: TECH & AI -->",
        '<td width="34%" style="border-right: 1px solid #cccccc; padding: 8px; font-size: 14px;">',
        '<div style="text-align: center; padding: 4px 0; background-color: #f0f0f0;">',
        '<font size="3"><b>TL;DR &mdash; TECH &amp; AI</b></font><br>',
        '<font size="1" color="#555555">What the machines are up to</font>',
        "</div>",
        "<hr>",
    ])

    if tech:
        for h in tech:
            lines.append(
                f"<b>{_link(h)}</b>"
                f'<br><font size="1" color="#666666">{h["source"]} | '
                f"{_time_ago(h['published'])}</font><br><br>"
            )
    else:
        lines.append("<b>NO TECH NEWS. THE MACHINES ARE SLEEPING.</b>")

    lines.extend([
        "</td>",
        "",
        "<!-- RIGHT COLUMN: MY PORTFOLIO -->",
        '<td width="33%" style="padding: 8px; font-size: 14px;">',
        '<div style="text-align: center; padding: 4px 0; background-color: #e8f5e9;">',
        '<font size="3"><b>MY PORTFOLIO</b></font><br>',
        '<font size="1" color="#555555">What your money is doing</font>',
        "</div>",
        "<hr>",
    ])

    if portfolio:
        for h in portfolio:
            lines.append(_portfolio_block(h))
    else:
        lines.append("<b>NO PORTFOLIO NEWS. YOUR MONEY IS FINE. PROBABLY.</b>")

    lines.extend([
        "</td>",
        "</tr>",
        "</table>",
        "",
        "<hr>",
        '<p style="text-align: center; font-size: 11px; color: #999999;">',
        "GRUDGE REPORT &copy; 2025. All links property of their respective owners.",
        "<br>Aggregated by robots. Read by patriots.",
        "</p>",
        "</body>",
        "</html>",
    ])

    return "\n".join(lines)
