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

6. Also add your App Store URL in `js/config.js`

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

The iOS app stays local — it is not on GitHub.

### GitHub Pages

1. Edit files in this `website/` folder locally
2. Copy changes into the `gpxviewer-website` repo and push to `main`
3. GitHub Actions deploys automatically
4. Custom domain is set in `CNAME` (`gpxviewerapp.com`). DNS at your registrar:

   | Type | Name | Value |
   |------|------|-------|
   | A | `@` | `185.199.108.153` |
   | A | `@` | `185.199.109.153` |
   | A | `@` | `185.199.110.153` |
   | A | `@` | `185.199.111.153` |
   | CNAME | `www` | `lucasdemap.github.io` |

5. In GitHub **Settings → Pages**, enable **Enforce HTTPS**

Your site will be live at `https://gpxviewerapp.com` (or `https://<user>.github.io/<repo>/` until DNS propagates).

### Other hosts

Upload the `website/` folder to Netlify, Vercel, or Cloudflare Pages if you prefer.

## Files

- `index.html` — landing page
- `privacy.html` — privacy policy (App Store / website)
- `js/config.js` — GA ID, App Store URL, contact email
- `js/analytics.js` — GA4 loader
- `js/site.js` — App Store links + click tracking
