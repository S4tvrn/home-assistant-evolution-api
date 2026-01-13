# 🚀 Evolution API WhatsApp Notifier for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

[🇮🇹 Italiano](#italiano) | [🇬🇧 English](#english)

---

<a name="italiano"></a>
## 🇮🇹 Italiano

Questa integrazione permette di inviare notifiche WhatsApp da **Home Assistant** utilizzando un'istanza di [Evolution API](https://doc.evolution-api.com/).

### ✨ Caratteristiche
- 📝 **Messaggi di testo**: Invia notifiche semplici a contatti o gruppi.
- 🖼️ **Immagini Locali**: Invia snapshot (es. da cartella `/config/www/` o `/media/`).
- 🌐 **Immagini da URL**: Invia immagini tramite link esterni.
- 🔑 **Sicurezza**: Supporto nativo per la `apikey` globale di Evolution.
- ⚡ **Affidabilità**: Gestione ottimizzata dei media rispetto ad altre soluzioni.

### ⚙️ Installazione via HACS
1. Apri **HACS** > **Integrazioni**.
2. Clicca sui tre puntini `⋮` in alto a destra e seleziona **Repository personalizzati**.
3. Incolla l'URL: `https://github.com/S4tvrn/home-assistant-evolution-api`.
4. Seleziona **Integrazione** e clicca su **Aggiungi**.
5. Scarica l'integrazione e **riavvia Home Assistant**.

### 🛠️ Configurazione YAML
Aggiungi al tuo file `configuration.yaml`:


notify:
  - name: whatsapp_evolution
    platform: evolution_notify
    url: "http://TUO_IP_EVOLUTION:8080"
    api_key: "TUA_GLOBAL_API_KEY"
    instance: "NOME_ISTANZA"