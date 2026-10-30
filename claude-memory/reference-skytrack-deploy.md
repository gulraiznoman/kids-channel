---
name: reference-skytrack-deploy
description: "SkyTrack deploy, local-dev, and headless-screenshot workflow and gotchas"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 03ef80f1-2ba8-4f17-927f-922ec9bc1880
  modified: 2026-07-28T12:28:49.222Z
---

Deploy / dev workflow for SkyTrack [[project-skytrack]]:

- Commit with `git user.email=gulraiznoman@yahoo.com` and NO `Co-Authored-By` trailer — Vercel Hobby rejects commits otherwise. A post-commit hook auto-pushes; if push fails (transient DNS), retry `git push origin HEAD:main` a few times.
- Confirm a deploy landed by polling the prod URL for the changed file (curl the js/css and grep a marker string added in that commit).
- Local dev server: `node server.js` (port 3000). It often stops between sessions; restart it before screenshotting.
- Screenshots: Edge headless — `msedge.exe --headless=new --disable-gpu --no-sandbox --window-size=W,H --virtual-time-budget=12000 --screenshot=OUT http://localhost:3000/...`. Deep-link a specific flight with `?sel=<hex>&lat=..&lon=..&z=..`. GOTCHA: headless renders at ~500px minimum CSS width even when window-size is smaller, so a 390px "mobile" shot is cropped from a wider render — not a real mobile bug.
- Inspect real trace data with: `curl "http://localhost:3000/api/trace?hex=<hex>"` and `curl "http://localhost:3000/api/flights?lamin=..&lomin=..&lamax=..&lomax=.."`.
- GOTCHA (Oct 2026): Vercel sometimes silently skips a pushed commit (prod stays on the previous build). If the marker string isn't live after ~3 min, push an empty commit (`git commit --allow-empty -m Redeploy`); it deployed in 45s. `gh` CLI is not installed and the repo is private, so the GitHub API can't show deploy status.
- Analytics hygiene (2026-10-12): every page loads `/js/analytics.js` (Cloudflare beacon). Add `?notrack=1` to EVERY test/screenshot URL I load against the live site so my checks don't inflate the user's visitor counts (Lighthouse is skipped automatically). Sitemap is now an index (`/sitemap.xml`) of sitemap-pages/-airports/-flights.xml, built by scripts/build-sitemap.mjs.
- Vercel Firewall (2026-10-13): custom rule "Block exploit scanners" (path regex -> Deny), Bot Protection = Log. Hitting denied paths ~14 times in a burst from the user's IP made a Vercel SYSTEM rule challenge that IP (looked like the whole site was down: 403 "Vercel Security Checkpoint", X-Vercel-Mitigated: challenge). Test blocked paths with ONE request at most; a 403 checkpoint from my machine usually means only the user's IP is challenged, not everyone. Don't create a permanent System Bypass for the user's (dynamic) home IP.
