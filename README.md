<div align="center">
  <img src="https://cdn.pensieriincodice.it/images/pensieriincodice-locandina.png" alt="Logo Progetto" width="150"/>
  <h1>Pensieri in codice — Episode to X</h1>
  <p>GitHub Action che pubblica automaticamente i nuovi episodi del podcast su X (Twitter).</p>
  <p>
    <img src="https://img.shields.io/github/stars/valeriogalano/pensieriincodice-episode-to-x?style=for-the-badge" alt="GitHub Stars"/>
    <img src="https://img.shields.io/github/forks/valeriogalano/pensieriincodice-episode-to-x?style=for-the-badge" alt="GitHub Forks"/>
    <img src="https://img.shields.io/github/last-commit/valeriogalano/pensieriincodice-episode-to-x?style=for-the-badge" alt="Last Commit"/>
    <a href="https://pensieriincodice.it/sostieni" target="_blank" rel="noopener noreferrer">
      <img src="https://img.shields.io/badge/sostieni-Pensieri_in_codice-fb6400?style=for-the-badge" alt="Sostieni Pensieri in codice"/>
    </a>
  </p>
</div>

---

## Come funziona

Il workflow controlla il feed RSS del podcast e pubblica i nuovi episodi sull'account X tramite le API ufficiali. Gli episodi già pubblicati vengono tracciati per evitare duplicati. Il workflow può essere attivato anche manualmente dalla scheda Actions.

---

## Requisiti

- Un account X con applicazione configurata per le API v2 (Bearer token)
- Un feed RSS del podcast

---

## Installazione e configurazione

### 1. Clona la repository

```bash
git clone https://github.com/YOUR_USERNAME/pensieriincodice-episode-to-x.git
cd pensieriincodice-episode-to-x
```

### 2. Configura i secrets di GitHub Actions

In **Settings → Secrets and variables → Actions**, aggiungi il seguente **Secret**:

| Secret | Descrizione |
|---|---|
| `X_TOKEN` | Bearer token dell'applicazione X (API v2) |

### 3. Configura le variabili di GitHub Actions

Nella stessa sezione, sotto la scheda **Variables**, aggiungi:

| Variabile | Descrizione |
|---|---|
| `PODCAST_RSS_URL` | URL del feed RSS del podcast (default: `https://pensieriincodice.it/podcast/index.xml`) |

### 4. Formato del messaggio

Il messaggio pubblicato ha un formato fisso (non configurabile tramite template):

```
🎙️ Nuovo episodio:
{titolo episodio}
{link episodio}
```

Tieni presente il limite di 280 caratteri per i post su X.

### 5. Sviluppo locale (opzionale)

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

---

## Contributi

Se noti qualche problema o hai suggerimenti, sentiti libero di aprire una **Issue** e successivamente una **Pull Request**. Ogni contributo è ben accetto!

---

## Importante

Vorremmo mantenere questo repository aperto e gratuito per tutti, ma lo scraping del contenuto di questo repository **NON È CONSENTITO**. Se ritieni che questo lavoro ti sia utile e vuoi utilizzare qualche risorsa, ti preghiamo di citare come fonte il podcast e/o questo repository.
