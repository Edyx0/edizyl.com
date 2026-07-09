interface Env {
  SPOTIFY_CLIENT_ID: string;
  SPOTIFY_CLIENT_SECRET: string;
  SPOTIFY_REFRESH_TOKEN: string;
  ALLOWED_ORIGIN?: string;
  ALLOWED_ORIGINS?: string;
}

const SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token';
const SPOTIFY_NOW_PLAYING_URL = 'https://api.spotify.com/v1/me/player/currently-playing';
const SPOTIFY_RECENTLY_PLAYED_URL = 'https://api.spotify.com/v1/me/player/recently-played?limit=1';

const getAllowedOrigin = (request: Request, env: Env) => {
  const origin = request.headers.get('Origin');
  if (!origin) return env.ALLOWED_ORIGIN || '*';

  const configuredOrigins = (env.ALLOWED_ORIGINS || env.ALLOWED_ORIGIN || '')
    .split(',')
    .map((value) => value.trim())
    .filter(Boolean);

  const isLocalDev = /^https?:\/\/(localhost|127\.0\.0\.1):\d+$/.test(origin);
  if (configuredOrigins.includes(origin) || isLocalDev) return origin;
  return configuredOrigins[0] || '*';
};

const json = (body: unknown, request: Request, env: Env, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: {
      'Access-Control-Allow-Origin': getAllowedOrigin(request, env),
      'Vary': 'Origin',
      'Access-Control-Allow-Methods': 'GET, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Cache-Control': 'public, max-age=20',
      'Content-Type': 'application/json; charset=utf-8',
    },
  });

const getAccessToken = async (env: Env) => {
  const basic = btoa(`${env.SPOTIFY_CLIENT_ID}:${env.SPOTIFY_CLIENT_SECRET}`);
  const body = new URLSearchParams({
    grant_type: 'refresh_token',
    refresh_token: env.SPOTIFY_REFRESH_TOKEN,
  });

  const response = await fetch(SPOTIFY_TOKEN_URL, {
    method: 'POST',
    headers: {
      Authorization: `Basic ${basic}`,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body,
  });

  if (!response.ok) throw new Error(`Spotify token error ${response.status}`);
  const data = await response.json<{ access_token?: string }>();
  if (!data.access_token) throw new Error('Spotify token missing access_token');
  return data.access_token;
};

const normalizeTrack = (item: any, isPlaying: boolean) => {
  const images = item?.album?.images || [];
  const albumImage = images[0]?.url || images[1]?.url || images[2]?.url || null;

  return {
    isPlaying,
    title: item?.name || null,
    artist: Array.isArray(item?.artists)
      ? item.artists.map((artist: any) => artist?.name).filter(Boolean).join(', ')
      : null,
    album: item?.album?.name || null,
    albumImage,
    spotifyUrl: item?.external_urls?.spotify || null,
  };
};

const fetchSpotifyJson = async (url: string, accessToken: string) =>
  fetch(url, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
      Accept: 'application/json',
    },
  });

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    if (request.method === 'OPTIONS') return json({}, request, env);
    if (request.method !== 'GET') return json({ error: 'Method not allowed' }, request, env, 405);

    try {
      const accessToken = await getAccessToken(env);
      const nowPlaying = await fetchSpotifyJson(SPOTIFY_NOW_PLAYING_URL, accessToken);

      if (nowPlaying.status === 200) {
        const data = await nowPlaying.json<any>();
        if (data?.item) {
          return json(normalizeTrack(data.item, Boolean(data.is_playing)), request, env);
        }
      }

      const recentlyPlayed = await fetchSpotifyJson(SPOTIFY_RECENTLY_PLAYED_URL, accessToken);
      if (recentlyPlayed.ok) {
        const data = await recentlyPlayed.json<any>();
        const item = data?.items?.[0]?.track;
        if (item) return json(normalizeTrack(item, false), request, env);
      }

      return json({ isPlaying: false, title: null, albumImage: null }, request, env);
    } catch (error) {
      return json(
        { error: error instanceof Error ? error.message : 'Spotify status failed' },
        request,
        env,
        500,
      );
    }
  },
};
