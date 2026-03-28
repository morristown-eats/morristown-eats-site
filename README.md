# Morristown Eats

The independent restaurant guide to Morristown, NJ.

## Setup

```bash
npm install
npm run dev        # local dev server at localhost:4321
npm run build      # build to /dist
npm run preview    # preview the build locally
```

## Deployment

Push to `main` → GitHub Actions builds and deploys automatically to GitHub Pages.

Before first deploy:
1. Go to your repo Settings → Pages → Source → set to "GitHub Actions"
2. Update `astro.config.mjs` with your GitHub Pages URL until your custom domain is live

## Adding a restaurant

Create a new file in `src/content/restaurants/your-restaurant-slug.md`.

Copy the frontmatter structure from any existing restaurant file.
Key fields:
- Set `published: false` while drafting
- Set `visit_status: "pending"` until you've visited
- Set `published: true` when ready to go live
- Add dishes and ratings after your visit
- Set `visit_status: "visited"` when the full profile is complete

Push to `main` → site rebuilds automatically in ~60 seconds.

## After visiting a restaurant

1. Update `visit_status` from `"pending"` to `"visited"`
2. Add `dishes` array with name + take for each recommendation
3. Add `ratings` (consistency, distinctiveness, execution, local_relevance — each 1–10)
4. Update the Markdown body with the full editorial take
5. Remove the "profile pending" language from the body
6. Update `last_visited` date
7. Push

## Fonts

Currently loading DM Serif Display and Inter from Google Fonts CDN.
For production: download WOFF2 files and self-host in `public/fonts/`.
Update `@font-face` declarations in `src/styles/global.css`.
