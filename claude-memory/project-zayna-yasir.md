---
name: project-zayna-yasir
description: "Zayna Yasir clothing brand (client): hand-embroidered PK womenswear, IG zayna.yasir, site zaynayasir.com; custom orders now, own collection later, min budget"
metadata:
  node_type: memory
  type: project
  originSessionId: cf669bef-a805-4a0b-809d-cd02ecdd8efb
  modified: 2026-10-26T18:14:21.265Z
---

Gulraiz is helping the brand Zayna Yasir (started 2026-10-26). They're doing custom dress orders now and want slow growth with minimal spend: dresses on the website, then ads, then their own collection.

- IG @zayna.yasir: ~587 followers, 62 posts, hand-embroidery reels, named pieces (Aghaz, Nazneen, Ruburo, Arzoo, Noor-e-Gul, Gulnaar Pink, Sage Bloom, Haya), WhatsApp 0324-8181846.
- Site zaynayasir.com: custom Next.js + Supabase build by Predigital.agency (not Shopify). As of 2026-10-26 it had only 6 products (Rs 13,999 to 32,990), none of the IG pieces, and "Let's Checkkkk" plus a 1234567 phone number in the HTML. WebFetch was WRONG twice here: the WhatsApp button works, and the Description/Details tabs do have content (they load when tapped). Have Gulraiz verify on screen before claiming any site issue. For a reliable audit, use headless Chrome + puppeteer-core (scratchpad/zy/audit*.js) and click the tabs. The 2026-10-26 headless audit confirmed: Midnight Rose + Verdant Bloom description = "Checking"; free-shipping banner but Rs 250 delivery at checkout; outdated Eid hero; footer categories that don't exist; generic meta description "Luxury fashion ecommerce and admin"; COD only.

Status 2026-10-26: the fix list was sent to Zayna. Zayna replied with a Rs 15,000/month ad budget and will update the website herself (hasn't worked on it before), and asked for portfolio + fee. I drafted a reply proposing Rs 15,000/month (first month Rs 10,000), a start date of 1 Nov, and no agency client names. Gulraiz decides the final fee. Next: product descriptions + custom order page for her to paste in, then the first ad plan.

**How to apply:** Don't use the browser to look at IG (see [[feedback-no-browser]]). Ask for screenshots, and use WebFetch for the site. Write copy plainly with no em dashes.
