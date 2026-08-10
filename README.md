# Paramjot Singh

**Full-stack engineer, applied AI.** I build products end to end — the model, the API, the interface, the installer, and the release that puts it on someone's machine.

Right now that means computer vision that runs on-device, marketplaces that move real money, and native macOS tools. Computer Science student at **Lovely Professional University**, Punjab, graduating 2028. Open to software engineering internships.

---

## Selected work

### [Vigil](https://github.com/Param077s/phone-detector) — AI phone detection for exam halls and secure areas
`Python` `YOLOv8` `FastAPI` `WebSockets` `OpenCV` `PyInstaller`

Watches any number of cameras — webcam, phone, or RTSP CCTV — and flags phones in real time with a cropped photo and location, for a human to confirm or dismiss. **All inference runs on-device; video never leaves the building**, which is what makes it deployable in a university at all.

Shipped as a **native desktop app for macOS, Windows and Linux** across **29 releases**, built and signed in CI. Includes a fine-tuning pipeline so an institution can sharpen the model on its own footage, a searchable evidence log with CSV export, role-based accounts, and a command palette.

→ **[Source](https://github.com/Param077s/phone-detector)** · [Download it](https://github.com/Param077s/vigil/releases/latest) · [Website](https://phone-detector-one.vercel.app)

---

### [Vouchroot](https://vouchroot.com) — marketplace for verified creator listings *(production)*
`React` `TypeScript` `Supabase/Postgres` `Stripe Connect` `Vercel`

A live commercial marketplace built on Stripe Connect. ~22,000 lines of TypeScript over 374 commits.

The part I would want to talk about in an interview is not the UI — it is the guardrails. Every database change goes through **13 CI workflows** including migration linting, a strict schema audit, an automated review of edge functions, and smoke tests against a preview deployment. When your code moves other people's money, "it works locally" is not a standard.

→ **[vouchroot.com](https://vouchroot.com)** · source private (commercial)

---

### [Foyer](https://github.com/Param077s/foyer) — paid conversations with escrow
`React 19` `TypeScript` `Supabase` `Row-Level Security` `GitHub Actions`

A creator sets a price to receive a message. A visitor pays to open a conversation, the money is held until the creator actually replies inside their promised window, and it refunds automatically if they don't.

The interesting constraint was authorization: with no server of my own, correctness has to live in **Postgres row-level security policies** rather than in application code that a client could route around. Every number shown on a creator's profile is computed by a database view — none of it is hand-set.

→ **[Live demo](https://foyer-murex.vercel.app)**

*Status: the full loop works; Stripe is not wired in yet and escrow is simulated. The README says so too.*

---

### [Superclip](https://github.com/Param077s/superclip) — a macOS clipboard that knows where the paste is going
`Swift` `AppKit` `Vision OCR` `Accessibility API`

Copy a table out of a PDF. Paste it into Numbers and you get real cells; into Slack, readable lines; into a code editor, an array literal. One copy, three correct outputs, and you never picked a format.

Nine global bindings — OCR any region of the screen, pull the value a field is asking for, spread one record across a whole form, build a copy stack and pop it field by field. Hotkeys are validated against both the app's own bindings and the system's, so a shortcut can never silently shadow another. **`⌘V` is deliberately untouchable** — no feature is worth adding latency to the most-pressed shortcut in computing.

*Status: early — it builds and runs, and the README is explicit about which paths are not yet exercised against real apps.*

---

### [Glimpse](https://github.com/Param077s/glimpse) — live window previews on the macOS Dock
`Swift 6` `ScreenCaptureKit` `Accessibility API`

Hover a Dock icon and see live thumbnails of that app's actual windows, then click straight through to one — the Windows taskbar behaviour, done natively. A background cache warmer keeps thumbnails current so the strip appears instantly instead of rendering under the cursor.

---

### [Stitch Book](https://github.com/Param077s/stitch-book) — bilingual order ledger for a tailoring shop
`React` `TypeScript` `i18n` `offline-first`

Customers, measurements per garment, orders with advance/balance, due dates and photos. Fully bilingual **English / ਪੰਜਾਬੀ**, and entirely offline — no account, no server, no internet.

Built for a real shop, which set every constraint: the person using it does not read English comfortably, has patchy connectivity, and will not create an account. Those constraints made it a better piece of software than any of my own preferences would have.

---

### [AdaptRes](https://param077s.github.io/adaptres/) — adaptive OS resource allocator
`JavaScript` `operating systems` `simulation`

Classic schedulers decide once: a process is admitted, gets a slice, and keeps it. AdaptRes runs a feedback loop instead — it measures CPU and memory pressure every tick and, when CPU crosses 88% or memory 83%, throttles the lowest-priority running process until the bottleneck clears. Nothing is killed and high-priority work is never touched; a throttled process recovers on its own once pressure drops.

Live Gantt chart, utilisation graphs, starvation detection and CSV metrics export — and an off switch for adaptive mode, so you can run the same load with static allocation and watch it degrade.

→ **[Run it in your browser](https://param077s.github.io/adaptres/)** — no install

---

### [Graph Algorithms Toolkit](https://github.com/Param077s/dsa-graph-project) — DSA fundamentals in C++
`C++17`

BFS, DFS, Dijkstra with path reconstruction, Prim's MST, cycle detection for directed and undirected graphs, and connected components — on a weighted adjacency list, in a menu-driven terminal program.

---

## Stack

**Languages** — Python · TypeScript · Swift · C++ · SQL

**AI / CV** — YOLOv8 · Ultralytics · OpenCV · PyTorch · model fine-tuning · on-device inference · vision-language model fallbacks

**Backend** — FastAPI · WebSockets · Supabase · PostgreSQL · row-level security · Stripe Connect · REST

**Frontend** — React 19 · Vite · TailwindCSS · i18n · offline-first

**Native** — Swift 6 · AppKit · ScreenCaptureKit · Vision · Accessibility API

**Infrastructure** — GitHub Actions · Vercel · Docker · PyInstaller · signed multi-platform releases

---

## How I work

- **Ship the whole thing.** A model in a notebook is not a product. Vigil is not finished because detection works — it is finished because someone can download a `.dmg`, drag it to Applications, and use it without a terminal.
- **Put the guardrails in CI.** Reviews catch what you thought to look for; pipelines catch what you didn't.
- **Be honest in the README.** Two of the projects above say plainly which parts are not finished. I would rather you trust the rest.

---

## Contact

- **Email** — [singhparamjot077s@gmail.com](mailto:singhparamjot077s@gmail.com)
- **Live work** — [vouchroot.com](https://vouchroot.com) · [Vigil](https://phone-detector-one.vercel.app)
- **Location** — Punjab, India
