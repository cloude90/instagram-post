# Istruzioni per Claude

Questo repo pubblica in automatico post su Instagram (profilo dell'utente) da `queue/`. L'utente NON è una nutrizionista: spiegazioni brevi e semplici.

## Cosa fai e cosa NON fai
- NON crei né modifichi foto: le foto le crea e le carica l'utente in `queue/`. Non puoi vedere il contenuto delle foto.
- Il tuo lavoro: scrivere le caption in `queue/<stesso-nome-della-foto>.txt` e controllare che la coda sia in ordine.
- Usa SOLO le informazioni che l'utente ti dà sulla foto. Non inventare argomenti, dati, storie, risultati, ingredienti o numeri. Se mancano informazioni, chiedile prima di scrivere.
- Niente consigli medici, diagnosi o promesse di risultato. L'utente non è una nutrizionista: non presentarla come tale.

## Formato
- Una caption per foto: `queue/FOTO1.jpg` -> `queue/FOTO1.txt` (stesso nome, estensione `.txt`).
- Il `.txt` contiene SOLO la caption (vedi "Stile delle caption"). NON aggiungere le frasi fisse né la CTA: le aggiunge `scripts/publish.py` da `config/`, insieme agli hashtag fissi (`config/hashtag.txt`, in fondo). Massimo 5 hashtag per post, e i 5 fissi sono già quelli: NON aggiungere altri hashtag nel `.txt`.
- Una CTA specifica per quel post, solo se richiesta, va dopo una riga con solo `---`.
- Non toccare `config/`, `scripts/` e `.github/` se non richiesto.

## Stile delle caption
- Lo scopo della caption è EDUCARE: dare informazioni utili, sempre dal punto di vista dell'esperienza diretta dell'utente ("nella mia esperienza...", "io ho imparato che..."), in prima persona.
- Lunghezza: 600-1200 caratteri (limite Instagram 2200 in tutto, comprese frasi fisse, CTA e hashtag). Paragrafi corti, righe vuote tra i blocchi, linguaggio semplice.
- Struttura: 1) prima riga che cattura (domanda o affermazione); 2) esperienza personale, usando solo ciò che l'utente racconta; 3) 3-5 punti pratici o spiegazioni semplici; 4) chiusura con un pensiero che rassicura.
- Racconta l'esperienza personale solo con i dettagli forniti dall'utente: non inventare vissuti, tempi, risultati o dati. Se per educare servono più dettagli (cosa ha provato, cosa le ha aiutato, errori fatti), chiedili.
- Informazioni generali: solo ciò che è affidabile e non medico; se non sei sicuro, chiedi all'utente. Mai diagnosi, cure, dosaggi o promesse di risultato. Meglio "per me ha funzionato / confrontati con la tua nutrizionista" che consigli generalizzati.

- Modelli di stile scritti dall'utente: cartella `esempi/` (non è la coda, non viene pubblicata). Leggili e imita tono, ritmo, elenchi puntati con "•" e prima persona. Gli esempi sono modelli di STILE, non contenuti da pubblicare. Tipi di struttura: racconto personale + elenco "Cosa ho capito"; oppure elenco di segnali/sintomi con etichetta in grassetto-stile ("Disturbi digestivi: ..."), chiusura con invito a non sottovalutare e a parlarne con un professionista. Terzo tipo (esempio 3): apertura con ✨ "Tutto quello che devi sapere:", 4-5 punti brevi con "•" (frasi secche, anche con → e parentesi), chiusura con 💛 e una frase personale in prima persona. Quarto tipo (esempio 4): breve e discorsivo, senza elenco: apertura con una frase netta + emoji (🌿), 2-3 paragrafi corti che partono da "nella mia esperienza", chiusura con il risultato personale. Non citare mai la dottoressa o fonti nel testo se l'utente non lo chiede. NON riusare i loro fatti (es. "6 mesi", percorso con la nutrizionista) in altre caption, se l'utente non li ripete per quel video.

## Dopo ogni modifica
- Controlla che ogni foto in `queue/` abbia il suo `.txt`.
- Fai commit e push su `main` (altrimenti il post non parte).
- Pubblicazione: 4 post a settimana (lun, mar, gio, sab verso le 12:30 ora italiana), in ordine alfabetico. Solo foto JPEG (no HEIC). Questo repo è PUBBLICO: non scrivere nulla di riservato.
