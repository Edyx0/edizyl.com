import { createServer } from 'node:http';

const clientId = process.env.SPOTIFY_CLIENT_ID;
const clientSecret = process.env.SPOTIFY_CLIENT_SECRET;
const port = Number(process.env.PORT || 8787);
const redirectUri = `http://127.0.0.1:${port}/callback`;
const scopes = ['user-read-currently-playing', 'user-read-recently-played'];

if (!clientId || !clientSecret) {
  console.error('Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET before running this script.');
  process.exit(1);
}

const exchangeCode = async (code) => {
  const basic = Buffer.from(`${clientId}:${clientSecret}`).toString('base64');
  const body = new URLSearchParams({
    grant_type: 'authorization_code',
    code,
    redirect_uri: redirectUri,
  });

  const response = await fetch('https://accounts.spotify.com/api/token', {
    method: 'POST',
    headers: {
      Authorization: `Basic ${basic}`,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body,
  });

  const data = await response.json();
  if (!response.ok) throw new Error(JSON.stringify(data));
  return data;
};

const authUrl = new URL('https://accounts.spotify.com/authorize');
authUrl.searchParams.set('client_id', clientId);
authUrl.searchParams.set('response_type', 'code');
authUrl.searchParams.set('redirect_uri', redirectUri);
authUrl.searchParams.set('scope', scopes.join(' '));

const server = createServer(async (request, response) => {
  try {
    const url = new URL(request.url || '/', redirectUri);
    const code = url.searchParams.get('code');

    if (!code) {
      response.writeHead(400, { 'Content-Type': 'text/plain; charset=utf-8' });
      response.end('Missing code. Start again from the printed Spotify URL.');
      return;
    }

    const token = await exchangeCode(code);
    response.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
    response.end('Refresh token created. You can close this tab and return to Terminal.');

    console.log('\nSPOTIFY_REFRESH_TOKEN=' + token.refresh_token);
    console.log('\nSave this as a Cloudflare Worker secret. Do not commit it.');
  } catch (error) {
    response.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
    response.end('Token exchange failed. Check Terminal.');
    console.error(error);
  } finally {
    server.close();
  }
});

server.listen(port, '127.0.0.1', () => {
  console.log('1. Add this Redirect URI in Spotify Developer Dashboard:');
  console.log(`   ${redirectUri}`);
  console.log('\n2. Open this URL, approve, and wait for the callback:');
  console.log(`   ${authUrl.toString()}`);
});
