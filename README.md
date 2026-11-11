# PSJA Good Eats — mobile setup

This is a **starter** that uses the November 2026 menu previously entered in the PSJA Good Eats HTML beta. **Verify each day against the official PDF** before relying on it. October and future months are not yet loaded. Bears and T-STEM currently share the same district menu as a placeholder; campus-specific availability has not been verified.

## Setup in Chrome on your phone
1. Sign in to GitHub and create a **private** repository. Upload `bot.py`, `menu.json`, `ratings.json`, and `.github/workflows/lunch.yml` preserving the folder structure. On mobile Chrome, enabling **Desktop site** may make file upload easier. You can also upload the files individually.
2. Open repository **Settings → Secrets and variables → Actions**. Add repository **secret** `DISCORD_BOT_TOKEN` with the token from the Discord Developer Portal. **Never paste it in chat or commit it to GitHub.** If you have shared it before, reset it.
3. Add repository **variable** `DISCORD_CHANNEL_ID` with the numeric channel ID. Optionally add `PING_BEARS` and `PING_TSTEM` as comma-separated **numeric Discord user IDs** (not names). Enable Discord Developer Mode to copy IDs.
4. Invite the existing bot to your server with **View Channel**, **Send Messages**, and **Read Message History** permissions. If it is already there, check those permissions.
5. Go to **Actions → PSJA Good Eats → Run workflow** and select `preview` first. Read the logs. Then select `post` to test a real message. Scheduled posts run at 6 AM America/Chicago on weekdays; GitHub can delay or occasionally skip scheduled workflows. GitHub may disable schedules on inactive public repositories, and free usage limits/policies can change.
6. Each new month, update `menu.json` with verified dates and meal choices. **Missing dates are labeled unavailable**, not invented.

## Corrections from your phone
Go to **Actions → PSJA Good Eats → Run workflow**. Choose `post`, enter a date, and optionally set `override_bears` or `override_tstem` to `good`, `bad`, `mid`, or `unrated`. To **edit** the original message rather than send another, enable Discord Developer Mode, copy that message's numeric ID and enter it in `edit_message_id`.

This is **not yet a Discord slash-command bot**. Slash commands require a separately hosted interaction endpoint (or a continuously running bot). GitHub Actions provides mobile-accessible manual correction controls instead.

## Menu source
November grades 9–12 PDF: https://resources.finalsite.net/images/v1793384134/psjaisdus/qwsiulnwudj3oxgvz6t2/NOV9TH-12THLUNCH.pdf
