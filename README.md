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
| `app_store_click` | User taps a store badge (`link_location`, `store` params) |

## Google Search Console

Connect Search Console so Google indexes **gpxviewerapp.com** and shows search performance.

### Option A — Verify with Google Analytics (easiest)

Your site already has GA4 (`G-MWGRHGCMJ8`). Use the **same Google account** that owns the Firebase/GA property.

1. Open [Google Search Console](https://search.google.com/search-console)
2. **Add property** → URL prefix → `https://gpxviewerapp.com`
3. Choose **Google Analytics** as the verification method
4. Click **Verify**

### Option B — HTML meta tag

1. In Search Console, choose **HTML tag** verification
2. Copy the `content` value from the meta tag (the long token string)
3. Paste it in `js/config.js`:

```js
searchConsoleVerification: "your-token-here",
```

4. Push to GitHub, then click **Verify** in Search Console

### Submit your sitemap

After verification:

1. Search Console → **Sitemaps**
2. Enter: `sitemap.xml`
3. Click **Submit**

Your full sitemap URL: **https://gpxviewerapp.com/sitemap.xml**

### Link Search Console to GA4

1. [Google Analytics](https://analytics.google.com/) → **Admin** → **Product links**
2. **Search Console links** → Link → select your property and `gpxviewerapp.com`

## SEO included on the site

- `robots.txt` and `sitemap.xml`
- Canonical URLs, Open Graph, and Twitter cards
- JSON-LD structured data (app, organization, FAQ)
- `og-image.jpg` for social previews
- Real app screenshots in hero and gallery

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
- `robots.txt` — crawler rules + sitemap link
- `sitemap.xml` — pages for Google
- `js/config.js` — GA ID, store URLs, Search Console token, site URL
- `js/seo.js` — Search Console meta tag injection
- `js/analytics.js` — GA4 loader
- `js/site.js` — store links + click tracking
- `images/` — app icon, screenshots, store badges, og-image
