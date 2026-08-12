# Day 9 Checklist — Real Provider Adapter

## Setup
- [ ] Merge Day 9 files
- [ ] Reinstall package
- [ ] Confirm version `0.9.0`
- [ ] Confirm `check-ai-provider --help` works

## Regression
- [ ] Run `python -m pytest`
- [ ] Confirm `49 passed`
- [ ] Confirm mock providers still work
- [ ] Confirm Day 8 gate still passes

## Secrets
- [ ] Understand `.env` vs `.env.example`
- [ ] Confirm `.env` is ignored
- [ ] Never commit a real API key
- [ ] Never paste a real API key into chat
- [ ] Never show a real API key in screenshots

## Optional Live Setup
- [ ] Copy `.env.example` to `.env`
- [ ] Set `OPENAI_API_KEY` locally
- [ ] Set `OPENAI_MODEL` locally
- [ ] Run `check-ai-provider --provider openai-live`
- [ ] Confirm key is reported only as configured/not configured
- [ ] Confirm network request says `NOT SENT`

## Optional Live Smoke Test
- [ ] Use Day 1 small pack first
- [ ] Explicitly select `--provider openai-live`
- [ ] Understand API usage/cost may occur
- [ ] Do not interpret one run as full security proof
