# The World Today: 23 November 2026

[![news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/scriptstealer/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/scriptstealer/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

A make.fun entry for **news-image-20261123** — sum up Monday 23 November 2026's
world news in one image. Referral code: `6rdgs9pm`.

## What it does

`main.py` (Python 3.13, no network) writes one 1024×1024 PNG to
`/output/entry.png`: a newspaper front page headed **THE WORLD TODAY**,
with a red date band reading **MONDAY, 23 NOVEMBER 2026**, a lead story on
Nvidia, and four more stories in a 2×2 grid. Every panel has a simple
pictorial illustration drawn procedurally, a short headline and one short
sub-line.

- **Primary path:** when Pillow is available, the page is drawn
  procedurally with PIL. The run is deterministic — two runs produce
  byte-identical output.
- **Fallback path:** when Pillow cannot be imported at all, `main.py`
  copies the pre-rendered `entry.png` bundled in this repository
  byte-for-byte to `/output/entry.png`.
- **Font loading is defensive:** the code tries several font files in
  several directories (overridable with `NEWS_FONT_DIR`) and falls back
  to PIL's built-in `ImageFont.load_default()` when no font file exists,
  so a missing font can never crash the program.

Run it with `python3 main.py` (or `MAKEFUN_OUTPUT_DIR=out python3 main.py`
to write somewhere other than `/output`).

## The five stories (all from Monday 23 November 2026)

1. **Huang is back at Nvidia** — Nvidia's board reinstated Jensen Huang
   as chief executive, less than two weeks after he stepped down; shares
   soared 31% in a day, the biggest one-day gain for a US company.
   Source: Reuters, "Nvidia reinstates Jensen Huang as CEO, igniting
   tech surge", 23 Nov 2026.
2. **US cuts Iran's "last lifeline"** — the US Treasury imposed sweeping
   new sanctions on more than two dozen Iranian exchange houses, front
   companies and operatives in Iran's shadow banking network.
   Source: Reuters, "US imposes sanctions on dozens linked to Iran's
   shadow banking networks", 23 Nov 2026.
3. **UK to host 2035 Women's World Cup** — FIFA's Extraordinary Congress
   confirmed England, Northern Ireland, Scotland and Wales as hosts of
   the 2035 FIFA Women's World Cup, the first World Cup staged in the UK
   since 1966. Source: FIFA / Reuters, 23 Nov 2026.
4. **Minister quits over AI exam cheat** — South Korea's education
   minister Choi Kyo-jin resigned, taking responsibility for confusion
   over last-minute measures against AI-assisted cheating in the
   Suneung college entrance exam. Source: Reuters, 23 Nov 2026.
5. **12,000 flee arena in gas scare** — more than 12,000 people were
   evacuated from Manchester's Co-op Live arena after an unknown
   substance was released during a Don Toliver concert; over 50 people
   were treated for eye and breathing symptoms. Source: CNN, 23 Nov 2026.

## License

MIT — see [LICENSE](LICENSE).
