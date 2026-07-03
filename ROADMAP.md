# Roadmap

Denne roadmapen gjør repoet klart for samarbeid, AI-agentarbeid og gradvis overgang fra idé til spillbar prototype.

## Fase 0 — Repo hygiene og samarbeid

Status: Påbegynt

- [x] Legg inn samarbeidsmodell
- [x] Legg inn PR- og issue-mal
- [x] Legg inn grunnleggende GitHub Actions-kontroll
- [ ] Rydd README til tydelig prosjektpitch
- [ ] Velg hovedspor: RDR2-inspirert narrativ, Nordheim GBA, Manus Universe Engine eller samlet R-I&S-univers

## Fase 1 — Konsept og vertikal slice

Mål: én liten spillbar eller simulerbar demonstrasjon.

- [ ] Definer hovedkarakterer og konflikt
- [ ] Definer første lokasjon
- [ ] Lag `docs/game_design.md`
- [ ] Lag `docs/world_bible.md`
- [ ] Lag `docs/vertical_slice.md`
- [ ] Lag første testscript/prototype

## Fase 2 — Automatisert produksjonsløype

Mål: alt arbeid skal kunne repeteres uten rot.

- [ ] CI kjører validering på hver PR
- [ ] Automatisk sjekk mot forbudte filer: ROM, saves, private keys, store binaries
- [ ] Automatisk docs-indeks
- [ ] Automatisk release-pakke for patcher/prototyper
- [ ] Manuell godkjenning før release

## Fase 3 — ASTRA-9 integrasjon

Mål: ASTRA-9 fungerer som strukturert analyseagent for univers, fysikk, NPC, historie og produktretning.

- [ ] Lag `docs/astra9_agent_brief.md`
- [ ] Lag prompt-register for faste agentoppgaver
- [ ] Lag mal for daglig prosjektstatus
- [ ] Lag mal for kode-/designreview
- [ ] Lag mal for IP- og idéproveniens

## Fase 4 — Prototypepakking

Mål: få ut testbare leveranser.

- [ ] Definer artefakter som kan publiseres trygt
- [ ] Legg inn `releases/README.md`
- [ ] Lag automatisk zip-pakke fra trygge filer
- [ ] Legg inn sjekkliste for iPhone/emulator/testing der relevant

## Regler for prioritering

1. Først ryddighet og reproduksjon.
2. Deretter én spillbar/minst simulerbar slice.
3. Deretter produksjonstempo.
4. Til slutt større universkoblinger.
