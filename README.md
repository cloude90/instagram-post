# Instagram Post (foto)

Pubblica foto singole su Instagram: lun, mer, ven, dom verso le 11:00.
Repo PUBBLICO (serve a Instagram per scaricare la foto): non metterci nulla di privato.

Per ogni post, in `queue/`: `NOME.jpg` + `NOME.txt` (caption). Solo JPEG, no HEIC.
La caption finale = frase iniziale + caption + frase finale + CTA + hashtag (da `config/`).
Per nessuna CTA: in fondo al `.txt` una riga `---` e sotto `NESSUNA`.
Secrets richiesti: `IG_USER_ID`, `IG_ACCESS_TOKEN`.
