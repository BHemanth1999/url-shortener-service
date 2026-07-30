# Demo Script — Business Cases

Use this during the interview to explain each feature with a real-world scenario.

---

## Feature 1: Create Short URL

**Business Case:** Marketing team sends SMS campaigns. SMS has 160-character limit. Long URLs waste space.

| Before | After |
|--------|-------|
| `https://www.adidas.com/summer-sale-2026/collections?utm_source=sms&ref=camp123` | `localhost:8000/summer26` |

**Demo:** Create a short URL with custom code "summer26" pointing to any website.

---

## Feature 2: Redirect

**Business Case:** Customer receives SMS with short link, clicks it, lands on the real page instantly.

**Demo:** Open `localhost:8000/summer26` in browser → redirects to original site.

---

## Feature 3: Analytics

**Business Case:** Marketing manager asks "How many people clicked our campaign link? Which day had most clicks?"

**Demo:** Check analytics → shows total clicks, clicks by date, visitor info.

---

## Feature 4: List All URLs

**Business Case:** Admin needs a dashboard to see all active links across all campaigns.

**Demo:** GET /api/urls → shows all links with pagination (page 1, 2, 3...).

---

## Feature 5: Bulk Create

**Business Case:** Marketing launches a campaign with 50 product links. They can't create one by one — need all at once.

**Demo:** Create 3 URLs in one request → all created instantly.

---

## Feature 6: Delete URL

**Business Case:** A campaign ended or a link was shared by mistake. Need to deactivate it immediately, but keep records for audit.

**Demo:** Delete a URL → link stops working (404), but data stays in database for compliance.

---

## Feature 7: Click Limit

**Business Case:** "First 50 customers get 30% off" — link should stop working after 50 clicks.

**Demo:** Create link with max_clicks=3 → works 3 times → 4th click gives "link expired".

---

## Feature 8: Expiration

**Business Case:** "Flash sale ends in 24 hours" — link should auto-deactivate after the sale ends.

**Demo:** Create link with expires_in_seconds=15 → works now → wait 15 sec → link dead.

---

## Feature 9: Password Protection

**Business Case:** Share a confidential document link with only your team. Only people with the password can access it.

**Demo:** Create link with password → without password gets rejected → with password works.

---

## Feature 10: URL Blocking

**Business Case:** Prevent hackers from using our platform to spread phishing/malware links to trick people.

**Demo:** Try to create link for `malware.com` → rejected automatically.

---

## Feature 11: Rate Limiting

**Business Case:** A bot tries to create thousands of links per minute to abuse our platform. Block it automatically.

**Demo:** After 10 requests in 1 minute → 11th gets rejected with "too many requests".

---

## How to Explain to Interviewer (30-second version)

> "I built a URL shortener — like Bitly — that covers 3 types of requirements:
>
> **CORE** (Greenfield): Basic link shortening, redirect, and analytics — built from scratch.
>
> **ACCESS CONTROL** (Brownfield): Added click limits, expiration, and passwords to control who can access links.
>
> **SECURITY** (Ambiguous): The requirement said 'make it secure' — I clarified it and added rate limiting and URL blocking.
>
> Everything is testable live through the Swagger UI."
