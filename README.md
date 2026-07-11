# GPX Viewer website

Static landing page for **gpxviewerapp.com** with Google Analytics 4.

## Setup Google Analytics

Use the **same Firebase project** as the iOS app (`gpx-reader-e5ba6`):

1. Open [Firebase Console](https://console.firebase.google.com/) → **gpx-reader-e5ba6**
2. Project settings → **Your apps** → **Add app** → **Web** (`</>`)
3. Register the site (e.g. `gpxviewerapp.com`)
4. Copy the **Measurement ID** (`G-XXXXXXXXXX`)
5. Paste it in `js/config.js`:

```js
gaMeasurementId: "G-XXXXXXXXXX",
```

6. Add your App Store and Google Play URLs in `js/config.js`

Web and app analytics will appear in the **same GA4 property**, so you can compare app vs website traffic.

### Custom events on the website

| Event | When |
|-------|------|
| `page_view` | Automatic |
| `app_store_click` | User taps a Download button (`link_location` param) |

## Local preview

```bash
cd website
python3 -m http.server 8080
```

Open http://localhost:8080

## Deploy

The live site repo is **public and website-only**:

**https://github.com/lucasdemap/gpxviewer-website**

Local clone: **`~/Desktop/gpxviewer-website`** — edit there and push to deploy.

The iOS app stays in the NavigationGPX project and is not on GitHub.

### GitHub Pages

1. Edit files in `~/Desktop/gpxviewer-website`
2. Push to `main` on GitHub — deploy runs automatically
3. Custom domain is set in `CNAME` (`gpxviewerapp.com`). DNS at your registrar:

   | Type | Name | Value |
   |------|------|-------|
   | A | `@` | `185.199.108.153` |
   | A | `@` | `185.199.109.153` |
   | A | `@` | `185.199.110.153` |
   | A | `@` | `185.199.111.153` |
   | CNAME | `www` | `lucasdemap.github.io` |

4. In GitHub **Settings → Pages**, enable **Enforce HTTPS**

Your site will be live at `https://gpxviewerapp.com` (or `https://<user>.github.io/<repo>/` until DNS propagates).

### Other hosts

Upload the `website/` folder to Netlify, Vercel, or Cloudflare Pages if you prefer.

## Files

- `index.html` — landing page
- `privacy.html` — privacy policy (App Store / website)
- `js/config.js` — GA ID, App Store & Play Store URLs, contact email
- `js/analytics.js` — GA4 loader
- `js/site.js` — store links + click tracking
