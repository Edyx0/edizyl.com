# Spotify Status Worker

This Cloudflare Worker returns the currently playing Spotify track, or the most recently played track when nothing is playing.

## Setup

1. Create a Spotify app at <https://developer.spotify.com/dashboard>.
2. Add this Redirect URI to the Spotify app settings:

   ```text
   http://127.0.0.1:8787/callback
   ```

3. Install Worker dependencies:

   ```bash
   cd spotify-worker
   npm install
   ```

4. Get a Spotify refresh token:

   ```bash
   SPOTIFY_CLIENT_ID="your-client-id" SPOTIFY_CLIENT_SECRET="your-client-secret" npm run get-refresh-token
   ```

5. Save secrets in Cloudflare:

   ```bash
   npx wrangler secret put SPOTIFY_CLIENT_ID
   npx wrangler secret put SPOTIFY_CLIENT_SECRET
   npx wrangler secret put SPOTIFY_REFRESH_TOKEN
   ```

6. Deploy:

   ```bash
   npm run deploy
   ```

7. Copy the deployed Worker URL and set it as the GitHub repository variable:

   ```text
   PUBLIC_SPOTIFY_STATUS_ENDPOINT=https://your-worker.your-subdomain.workers.dev
   ```

The portfolio reads `albumImage` from this endpoint and shows it in the center of the Music record on hover.
