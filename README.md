
# 🚀 Evolution API WhatsApp Notifier for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Home Assistant](https://img.shields.io/badge/Home_Assistant-2023.6.0+-blueviolet.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

[🇮🇹 Italiano](#italiano) | [🇬🇧 English](#english)

---

<a name="italiano"></a>
## 🇮🇹 Italiano

Questa integrazione personalizzata permette di inviare notifiche WhatsApp da **Home Assistant** utilizzando un'istanza di [Evolution API](https://doc.evolution-api.com/). È progettata per essere leggera, veloce e supportare l'invio di contenuti multimediali sia locali che remoti.

### ✨ Caratteristiche
- 📝 **Messaggi di testo**: Invia notifiche semplici a contatti singoli o gruppi.
- 📸 **Immagini Locali**: Supporto per l'invio di file salvati in Home Assistant (es. snapshot delle telecamere).
- 🌐 **Immagini da URL**: Invia immagini tramite link pubblici.
- 🔑 **Sicurezza**: Integrazione nativa con la Global API Key di Evolution.
- ⚡ **Affidabilità**: Gestione dei media ottimizzata tramite multipart/form-data.

### ⚙️ Installazione via HACS
1. Assicurati che **HACS** sia installato sul tuo Home Assistant.
2. Vai in **HACS** > **Integrazioni**.
3. Clicca sui tre puntini `⋮` nell'angolo in alto a destra e seleziona **Repository personalizzati**.
4. Incolla l'URL del tuo repository: `https://github.com/S4tvrn/home-assistant-evolution-api`.
5. Seleziona la categoria **Integrazione** e clicca su **Aggiungi**.
6. Cerca "Evolution API WhatsApp", clicca su **Scarica** e **riavvia Home Assistant**.

### 🛠️ Configurazione YAML
Aggiungi la seguente configurazione al tuo file `configuration.yaml`:

| Parametro | Descrizione |
|-----------|-------------|
| `version` | (Opzionale) La versione della tua Evolution API. Usa `1` per versioni 1.x (es. 1.8.2) o `2` per le versioni più recenti. Default: `1`. |


```yaml
notify:
  - name: whatsapp_evolution
    platform: evolution_notify
    url: "http://192.168.1.XXX:8080"
    api_key: "TUA_API_KEY"
    instance: "TUA_ISTANZA"
    version: 1  # <--- Specifica 1 per Evolution v1.x, 2 per Evolution v2.x
```

### 🚀 Esempi di Utilizzo

#### 1. Messaggio di testo semplice
```yaml
service: notify.whatsapp_evolution
data:
  target: "391234567890"
  message: "🚨 Allarme! Porta d'ingresso aperta."
```

#### 2. Invio Snapshot Camera (File Locale)
```yaml
service: notify.whatsapp_evolution
data:
  target: "391234567890"
  message: "📸 Movimento rilevato in giardino"
  data:
    path: "/config/www/snapshots/garden.jpg"
```

#### 3. Immagine da URL
```yaml
service: notify.whatsapp_evolution
data:
  target: "391234567890"
  message: "Ecco il grafico meteo"
  data:
    image: "https://vostrosito.it/meteo.png"
```

---

<a name="english"></a>
## 🇬🇧 English

This custom integration allows you to send WhatsApp notifications from **Home Assistant** using an [Evolution API](https://doc.evolution-api.com/) instance. It is designed to be lightweight, fast, and supports both local and remote multimedia content.

### ✨ Features
- 📝 **Text Messages**: Send simple notifications to individual contacts or groups.
- 📸 **Local Images**: Support for sending files stored in Home Assistant (e.g., camera snapshots).
- 🌐 **Images via URL**: Send images through public links.
- 🔑 **Security**: Native integration with Evolution's Global API Key.
- ⚡ **Reliability**: Optimized media handling via multipart/form-data.

### ⚙️ Installation via HACS
1. Ensure **HACS** is installed on your Home Assistant.
2. Go to **HACS** > **Integrations**.
3. Click the three dots `⋮` in the top right corner and select **Custom repositories**.
4. Paste the repository URL: `https://github.com/S4tvrn/home-assistant-evolution-api`.
5. Select **Integration** as the category and click **Add**.
6. Find "Evolution API WhatsApp", click **Download**, and **restart Home Assistant**.

### 🛠️ YAML Configuration
Add the following configuration to your `configuration.yaml` file:

```yaml
notify:
  - name: whatsapp_evolution
    platform: evolution_notify
    url: "http://192.168.1.XXX:8080"      # Your Evolution API instance URL
    api_key: "YOUR_GLOBAL_API_KEY"       # Your Global API Key
    instance: "INSTANCE_NAME"             # The instance name created in Evolution
```

### 🚀 Usage Examples

#### 1. Simple Text Message
```yaml
service: notify.whatsapp_evolution
data:
  target: "391234567890"
  message: "🚨 Alarm! Front door opened."
```

#### 2. Send Camera Snapshot (Local File)
```yaml
service: notify.whatsapp_evolution
data:
  target: "391234567890"
  message: "📸 Motion detected in the garden"
  data:
    path: "/config/www/snapshots/garden.jpg"
```

---

### ⚠️ Troubleshooting & Notes
- **Target format**: Use the international format without the `+` sign (e.g., `391234567890`).
- **Folders**: For local files, ensure the folder is in the Home Assistant `allowlist_external_dirs` if it's outside the standard `www` folder.
- **Instance**: Ensure your Evolution instance is "connected" (QR code scanned) before sending messages.


**Developed with ❤️ by [S4tvrn](https://github.com/S4tvrn)**

