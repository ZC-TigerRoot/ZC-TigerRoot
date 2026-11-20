"""Generate the profile header SVGs (dark + light).

Usage:  python scripts/build_header.py
Writes assets/header-dark.svg and assets/header-light.svg.
Pure SVG + CSS: no external fonts or services, so GitHub renders it as-is.
"""

import random
from pathlib import Path

W, H = 1200, 300
CX, CY = 905, 150  # black hole centre

SANS = "'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei','Noto Sans CJK SC',sans-serif"
MONO = "ui-monospace,'SFMono-Regular','Cascadia Code',Consolas,Menlo,monospace"

THEMES = {
    "dark": dict(
        bg="#0b0d12", star="#e5e7eb", star_op=(0.15, 0.7),
        accent="#f59e0b", title="#f3f4f6", sub="#9ca3af",
        body="#d1d5db", muted="#6b7280", faint="#4b5563",
        glow_op=0.22, shadow="#000000", ring="#ffe8c2",
    ),
    "light": dict(
        bg="#f7f5f0", star="#1f2937", star_op=(0.08, 0.3),
        accent="#c2410c", title="#111827", sub="#6b7280",
        body="#374151", muted="#6b7280", faint="#9ca3af",
        glow_op=0.16, shadow="#0b0d12", ring="#fff3dc",
    ),
}


def stars(t):
    rnd = random.Random(7)
    out = []
    for i in range(70):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        r = rnd.choice([0.6, 0.8, 1.0, 1.3])
        op = rnd.uniform(*t["star_op"])
        cls = ' class="tw"' if i % 6 == 0 else ""
        delay = f' style="animation-delay:{rnd.uniform(0, 4):.1f}s"' if cls else ""
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{t["star"]}" opacity="{op:.2f}"{cls}{delay}/>')
    return "\n    ".join(out)


def disk(extra=""):
    """Accretion disk: solid gradient band + dashed overlay that drifts (rotation hint)."""
    return f"""<g{extra}>
      <ellipse cx="{CX}" cy="{CY}" rx="200" ry="24" fill="none" stroke="url(#disk)" stroke-width="11"/>
      <ellipse cx="{CX}" cy="{CY}" rx="200" ry="24" fill="none" stroke="#fff" stroke-opacity=".35"
               stroke-width="3" stroke-dasharray="2 14" class="spin"/>
      <ellipse cx="{CX}" cy="{CY}" rx="232" ry="30" fill="none" stroke="url(#disk)" stroke-width="2" opacity=".45"/>
    </g>"""


def render(name, t):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
  <title id="t">TigerRoot · ZC-TigerRoot</title>
  <desc id="d">Evidence-first data systems, LLM tooling and real-time graphics. A black hole with an accretion disk on the right.</desc>
  <style>
    .tw {{ animation: tw 4s ease-in-out infinite; }}
    .spin {{ animation: spin 9s linear infinite; }}
    .pulse {{ animation: pulse 6s ease-in-out infinite; transform-origin: {CX}px {CY}px; }}
    @keyframes tw {{ 50% {{ opacity: .05; }} }}
    @keyframes spin {{ to {{ stroke-dashoffset: -320; }} }}
    @keyframes pulse {{ 50% {{ opacity: .7; }} }}
    @media (prefers-reduced-motion: reduce) {{ .tw, .spin, .pulse {{ animation: none; }} }}
  </style>
  <defs>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#f59e0b" stop-opacity="{t['glow_op']}"/>
      <stop offset=".55" stop-color="#ea580c" stop-opacity="{t['glow_op'] / 3:.3f}"/>
      <stop offset="1" stop-color="#ea580c" stop-opacity="0"/>
    </radialGradient>
    <!-- left side brighter: Doppler beaming of the approaching side -->
    <linearGradient id="disk" x1="0" x2="1">
      <stop offset="0" stop-color="#7c2d12" stop-opacity=".2"/>
      <stop offset=".18" stop-color="#fbbf24"/>
      <stop offset=".32" stop-color="#fff7e6"/>
      <stop offset=".55" stop-color="#f59e0b"/>
      <stop offset=".82" stop-color="#9a3412"/>
      <stop offset="1" stop-color="#7c2d12" stop-opacity=".2"/>
    </linearGradient>
    <linearGradient id="lens" x1="0" x2="1">
      <stop offset="0" stop-color="#fbbf24"/>
      <stop offset=".4" stop-color="#fff7e6"/>
      <stop offset="1" stop-color="#c2410c"/>
    </linearGradient>
    <clipPath id="front"><rect x="0" y="{CY}" width="{W}" height="{H - CY}"/></clipPath>
  </defs>

  <rect width="{W}" height="{H}" fill="{t['bg']}"/>
  <g>
    {stars(t)}
  </g>

  <!-- black hole -->
  <circle cx="{CX}" cy="{CY}" r="190" fill="url(#glow)" class="pulse"/>
  {disk()}
  <circle cx="{CX}" cy="{CY}" r="76" fill="none" stroke="url(#lens)" stroke-width="5" opacity=".8"/>
  <!-- far side of the disk, lensed up and over the shadow -->
  <path d="M{CX - 78},{CY} A78 90 0 0 1 {CX + 78},{CY} L{CX + 74},{CY} A74 74 0 0 0 {CX - 74},{CY} Z" fill="url(#lens)" opacity=".6"/>
  <circle cx="{CX}" cy="{CY}" r="64" fill="{t['shadow']}"/>
  <circle cx="{CX}" cy="{CY}" r="65.5" fill="none" stroke="{t['ring']}" stroke-width="1.2" opacity=".9"/>
  {disk(' clip-path="url(#front)"')}

  <!-- text -->
  <g font-family="{SANS}">
    <text x="72" y="84" font-family="{MONO}" font-size="15" letter-spacing="2" fill="{t['accent']}">// ZC-TigerRoot</text>
    <rect x="72" y="98" width="36" height="2" fill="{t['accent']}"/>
    <text x="68" y="160" font-size="64" font-weight="700" letter-spacing="-1" fill="{t['title']}">TigerRoot</text>
    <text x="72" y="204" font-size="20" fill="{t['body']}">证据优先的数据系统 · LLM 工具链 · 实时图形</text>
    <text x="72" y="234" font-family="{MONO}" font-size="14.5" fill="{t['muted']}">Evidence-first systems · LLM tooling · Real-time graphics</text>
    <text x="72" y="266" font-family="{MONO}" font-size="12.5" letter-spacing="1" fill="{t['faint']}">SINCE 2020  ·  BUILDING IN PUBLIC</text>
  </g>
</svg>
"""
    return svg


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets"
    out.mkdir(exist_ok=True)
    for name, t in THEMES.items():
        (out / f"header-{name}.svg").write_text(render(name, t), encoding="utf-8")
        print("wrote", out / f"header-{name}.svg")
