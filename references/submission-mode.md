# Optional FlatPark catalog submission mode — explicit user request only

This mode is NOT activated by generic phrasing like "package this app". Only use when the user explicitly wants to submit it to FlatPark or prepare a catalog PR. Begin with the current https://flatpark.org/docs/packagers/playbook/ and check all linked rules.

1. Candidate research: existing Flathub publication (and who maintains it), prior Flatpak requests, legitimate vendor origin and demand.
2. Eligibility: stable official Linux download URL, runnable core functionality in sandbox, current supported runtime, policy/rights, correct ID; FlatPark's detailed Flathub overlap and upstream-maintained packages rules apply (even though personal mode does not enforce them).
3. Use actual `flatpark/flatpark` checkout and its `AGENTS.md`, `docs/README.md`, `registry/<app-id>`, current example packages and `scripts/`. One package per PR. Follow update resolver and manifest protocols exactly; submit `flatpark.yml`, manifest, install script, wrapper, icon, desktop, metainfo and resolver as appropriate.
4. Mechanical validation **inside FlatPark repo** (confirm script names in current repo first):

   ```sh
   node scripts/read-descriptor.mjs registry/APP_ID/flatpark.yml
   node scripts/audit-descriptor.mjs registry/APP_ID/flatpark.yml
   ./scripts/check-apply-extra.sh APP_ID
   ./scripts/publish.sh --verify APP_ID
   ```

   Where supported, `FLATPARK_VERIFY_KEEP=1 ./scripts/publish.sh --verify APP_ID` keeps the test install for actual GUI feature/restart checks. Use a unique app test ID/profile strategy if existing user data might collide. Do not invoke the scripts blindly in a standalone personal folder.
5. Run every currently required check from official Testing Playbook. If main feature cannot be tested, submission is blocked until a capable tester/upstream verifies it. Record accurate test limitations.
6. Prepare branch/commit/PR following current submitting instructions; show **exact PR title and body** and ask for **separate explicit approval before opening PR**. No misleading upstream claims, no unstated package modifications, no pretending upstream approved. Do not push or publish unless the user directed it; the official playbook's branch/push allowances do not replace the user's own preferences.
7. **Contact upstream only after the package is live, used, and separately approved for contact**. Draft a short accurate message: what FlatPark package does, how to install, partial testing scope, optional link request, clear opt-out. Don't characterize the upstream app as broken or imply consent. Consult current playbook contact tracker before outreach; do not spam.
8. On upstream reply, honor modifications/corrections or delist requests; never repost after an explicit no. Maintenance follows current update-check/re-pin protocols, and keep supported runtime/stack pinning up to date.

**Publication actions are never automatic in this skill**, including PRs, issues, releases and remote uploads. A personal-use package can remain local even when FlatPark policy would reject its inclusion; do not misrepresent it as a catalog package.
