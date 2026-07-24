from __future__ import annotations

from collections.abc import Mapping


def _quote(value: str) -> str:
    """
    Quote a RouterOS string literal.

    RouterOS strings use double quotes and escaped quotes.
    """

    return (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
    )


def serialize_json(
    variable_name: str,
    fields: Mapping[str, str],
) -> str:
    """
    Generate RouterOS code that creates a map and serializes it to JSON.

    Example output:

        :local event ({
            "event"="hotspot.login";
            "username"=$username;
        })

        :local payload [:serialize \
            value=$event \
            to=json \
            options=json.no-string-conversion]
    """

    lines: list[str] = []

    lines.append(f":local {variable_name} ({{")

    for key, value in fields.items():
        if value.startswith("$"):
            rendered = value
        elif value in {
            "true",
            "false",
            "nil",
        }:
            rendered = value
        elif value.replace(".", "", 1).isdigit():
            rendered = value
        else:
            rendered = f'"{_quote(value)}"'

        lines.append(
            f'    "{_quote(key)}"={rendered};'
        )

    lines.append("})")
    lines.append("")
    lines.append(
        ":local payload [:serialize \\"
    )
    lines.append(
        f"    value=${variable_name} \\"
    )
    lines.append(
        "    to=json \\"
    )
    lines.append(
        "    options=json.no-string-conversion]"
    )

    return "\n".join(lines)