from pathlib import Path
import shutil
import sys

from jinja2 import (
    Environment,
    FileSystemLoader,
)

# ==========================================================
# Project Root
# ==========================================================

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

sys.path.insert(
    0,
    str(PROJECT_ROOT),
)

# ==========================================================
# Application Imports
# ==========================================================

from app.router_portal.context_builder import (  # noqa: E402
    RouterPortalContextBuilder,
)

from app.router_portal.template_context import (  # noqa: E402
    PortalTemplateContext,
)

# ==========================================================
# Paths
# ==========================================================

PORTAL_ROOT = (
    PROJECT_ROOT
    / "app"
    / "router_portal"
)

TEMPLATES_DIR = (
    PORTAL_ROOT
    / "templates"
)

STATIC_DIR = (
    PORTAL_ROOT
    / "static"
)

DIST_DIR = (
    PROJECT_ROOT
    / "dist"
)

ROUTEROS_DIR = (
    DIST_DIR
    / "routeros"
)

OUTPUT_DIR = (
    ROUTEROS_DIR
    / "hotspot"
)

# ==========================================================
# Templates To Build
# ==========================================================

HOTSPOT_TEMPLATES = {

    # ======================================================
    # BryanNet
    # ======================================================

    "error.html": "error.html",

    "login.html": "login.html",

    "logout.html": "logout.html",

    "router_login.html": "router_login.html",

    "status.html": "status.html",

    # ======================================================
    # RouterOS
    # ======================================================

    "alogin.html": "alogin.html",

    "radvert.html": "radvert.html",

    "redirect.html": "redirect.html",

    "rlogin.html": "rlogin.html",

}

# ==========================================================
# Jinja Environment
# ==========================================================

environment = Environment(

    loader=FileSystemLoader(
        TEMPLATES_DIR,
    ),

    autoescape=True,

)

# ==========================================================
# Render Template
# ==========================================================


def render_template(
    template_name: str,
    output_name: str,
) -> None:

    hotspot = (
        RouterPortalContextBuilder
        .from_preview()
    )

    context = (
        PortalTemplateContext
        .build(

            hotspot=hotspot,

            request=None,

            static_url=".",

            build_mode=True,

            username="preview-user",

            password="preview-password",

        )
    )

    template = (
        environment
        .get_template(
            template_name,
        )
    )

    html = template.render(
        **context,
    )

    output_file = (
        OUTPUT_DIR
        / output_name
    )

    output_file.write_text(

        html,

        encoding="utf-8",

    )

    print(
        f"✓ Generated {output_name}"
    )


# ==========================================================
# Copy Static Assets
# ==========================================================


def copy_static() -> None:

    for item in STATIC_DIR.iterdir():

        destination = (
            OUTPUT_DIR
            / item.name
        )

        if destination.exists():

            if destination.is_dir():

                shutil.rmtree(
                    destination,
                )

            else:

                destination.unlink()

        if item.is_dir():

            shutil.copytree(

                item,

                destination,

            )

        else:

            shutil.copy2(

                item,

                destination,

            )

    print(
        "✓ Copied static assets"
    )

# ==========================================================
# Prepare Output Directory
# ==========================================================


def prepare_output() -> None:

    if OUTPUT_DIR.exists():

        shutil.rmtree(
            OUTPUT_DIR,
        )

    OUTPUT_DIR.mkdir(

        parents=True,

        exist_ok=True,

    )


# ==========================================================
# Main
# ==========================================================


def main() -> None:

    print()

    print("=" * 60)
    print("Building RouterOS Hotspot Package")
    print("=" * 60)

    prepare_output()

    print()

    print("Rendering templates...")

    for template, output in HOTSPOT_TEMPLATES.items():

        render_template(

            template,

            output,

        )

    print()

    print("Copying static assets...")

    copy_static()

    print()

    print("=" * 60)
    print("✓ Hotspot package built successfully.")
    print(f"✓ Output: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":

    main()