# Roteiro do diretor — `assets/scenes.yaml`

O planner escolhe cenas sozinho (letra → tags → cena, energia da música, sem repetir).
Quando você (ou eu, como diretor) quiser **forçar** uma cena num trecho, use o roteiro.

```yaml
scenes:
  # por trecho da letra (casa com a linha que contém esse texto)
  - line: "o sharingan desperta"
    assets: [olho_close, "ep12_cena#004"]   # ids de assets/assets.yaml (ou nome do arquivo sem #)
    note: close nos olhos no despertar

  # por tempo (mm:ss ou segundos)
  - at: "1:12"
    until: "1:20"
    tags: [itachi, emotional, rain]          # dá preferência forte a essas tags
```

## Tags que o sistema entende

`closeup, eyes, battle, transformation, emotional, calm, tension, impact, power, rain, flashback,
villain, duo, crowd, dark, light, fire, lightning, blood, smile, scream, run, fall, sky, domain`
+ qualquer tag própria (ex.: `itachi`, `naruto`) — se a palavra aparece na letra, a cena ganha pontos.

## Como a letra vira cena

1. `configs/characters/<char>.yaml → tag_map`: palavra da letra → tags (ex.: `chidori → lightning, battle`).
2. Palavras marcadas com `*asterisco*` na letra valem o dobro.
3. Trechos com citação forte escolhem cena **primeiro**; o resto preenche em volta, sem repetir
   a mesma cena a menos de 3 planos de distância.

## Excluir uma cena

Em `assets/assets.yaml`, adicione `use: never` no item.
