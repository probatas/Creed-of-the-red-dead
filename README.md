# Cubone-utgave for Pokémon FireRed 1.0

Dette prosjektet lager en `.gba`-fil **lokalt** fra din egen, lovlig anskaffede
kopi av **Pokémon FireRed (USA) v1.0**. Nintendo-spillet følger ikke med i
prosjektet og lastes ikke ned av skriptet.

> **Prosjektstatus:** Dette repositoryet inneholder foreløpig bare en
> frittstående ROM-headerprototyp. Det er ikke selve `pret/pokefirered`-
> kildetreet og inneholder derfor ikke kart-, encounter- eller storyendringene
> til Pokémon Cubone-prosjektet.

Foreløpig endring er bevisst liten og trygg: ROM-tittelen endres til
`CUBONE FIRE`, og GBA-headerens kontrollsum beregnes på nytt. `cubone_info.py`
inneholder Cubone-oppslagsdataene fra første versjon av prosjektet; disse er
ikke dialog i spillet ennå.

## Lag `.gba`-filen

1. Dump din egen FireRed-kassett som en `.gba`-fil.
2. Kontroller at det er den amerikanske 1.0-utgaven. Skriptet krever SHA-1
   `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` og avviser alle andre filer.
3. Åpne terminalen i VS Code i denne mappen og kjør:

   ```bash
   python firered_cubone_patch.py FireRed.gba
   ```

Da opprettes:

* `Cubone-FireRed.gba` – den spillbare filen du kan åpne i en GBA-emulator.
* `Cubone-FireRed.ips` – en liten, delbar patch uten originalspilldata.

Velg andre filnavn ved behov:

```bash
python firered_cubone_patch.py FireRed.gba -o mitt-spill.gba --ips mitt-spill.ips
```

Input-ROM, output-ROM og IPS-patch må bruke tre forskjellige filstier. Skriptet
avviser kollisjoner før det skriver noe, slik at originaldumpen ikke
overskrives. `.gitignore` hindrer også at ROM- og emulatorlagringsfiler blir
lagt til i Git ved et uhell.

## Hvorfor ligger ingen ferdig `.gba` her?

En ferdig FireRed-ROM inneholder opphavsrettsbeskyttet spillkode og grafikk.
Derfor leverer repoet et verktøy og en IPS-patchgenerator i stedet. Når du
kjører kommandoen med din egen dump, får du den etterspurte `.gba`-filen på
maskinen din uten at originalspillet distribueres.

## Test

```bash
python -m unittest -v
```
