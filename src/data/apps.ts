export interface AppData {
  slug: string;
  name: string;
  subtitle: string;
  tagline: string;
  icon: string;
  accent: string;
  appStoreUrl: string;
  short: string;
  about: string[];
  features: string[];
  stack: { label: string; value: string }[];
  techChips: string[];
  builtStory: string[];
  highlights?: string[];
  stats?: { label: string; value: string }[];
  previewVideoHls?: string;
  previewVideoPoster?: string;
  screenshots: string[];
  meta: {
    version: string;
    released: string;
    updated: string;
    minOS: string;
    size: string;
    genre: string;
    rating?: string;
  };
}

export const apps: AppData[] = [
  {
    slug: 'tabu-ekstra',
    name: 'Tabum Ekstra',
    subtitle: '2026 Kelimeleri',
    tagline: 'A fast, offline 2026 word game for friends, family, school, and campus groups.',
    icon: '/icons/tabu-ekstra.png',
    accent: '#9d4edd',
    appStoreUrl: 'https://apps.apple.com/tr/app/tabum-ekstra-2026-kelimeleri/id6757464030',
    short: 'Offline 2026 word game for party play. Current App Store version: 1.8.2 with a 4.5 rating from 36 reviews.',
    about: [
      "Tired of playing games with boring, old-school words? Tabum Ekstra brings the trendiest and most original terms of 2026 right to your pocket, ready for family, friends, school, campus, or anywhere.",
      "It is built for free offline play, with cards designed to sharpen thinking, expand vocabulary, and boost general knowledge while keeping the pace light and social.",
    ],
    features: [
      'Curated 2026 word cards, refreshed regularly',
      'Offline play for family, friends, school, and campus groups',
      'Turkish, German, and English word lists',
      'Vocabulary, quick thinking, and general knowledge focus',
    ],
    techChips: ['Swift 5', 'SwiftUI', 'StoreKit 2', 'Google AdMob', 'RevenueCat', 'PlayFab', 'Figma', 'Procreate', 'iOS 15.6+'],
    stack: [
      { label: 'Language', value: 'Swift 5' },
      { label: 'UI', value: 'SwiftUI' },
      { label: 'Persistence', value: 'JSON wordlists, UserDefaults' },
      { label: 'Monetization', value: 'Google AdMob (interstitial + rewarded), RevenueCat-managed StoreKit 2 subscriptions' },
      { label: 'Analytics', value: 'PlayFab (Microsoft)' },
      { label: 'Design', value: 'Figma, Procreate' },
      { label: 'Localization', value: 'String Catalogs (TR · DE)' },
      { label: 'Min iOS', value: '15.6' },
    ],
    builtStory: [
      'Built in SwiftUI for iOS 15.6+, Tabum Ekstra ships a curated 2026 word list as JSON and renders cards with subtle physics-driven animations. The current App Store positioning focuses on free offline play, fresh 2026 terms, and quick sessions for family, friends, school, campus, or anywhere.',
      'The app combines Google AdMob with StoreKit 2 subscriptions managed via RevenueCat for cross-device entitlement sync. PlayFab handles lightweight analytics and fast content management so word list updates can ship quickly while the App Store build stays stable.',
    ],
    highlights: [
      '#18 in Card Games (Turkey)',
      'Version 1.8.2, updated July 2, 2026',
      '4.5 App Store rating across 36 reviews',
      'Offline 2026 word game for groups',
    ],
    stats: [
      { label: 'App Store rank - All time high', value: '#8 TR Card Games' },
      { label: 'Rating', value: '4.5 ★ (36)' },
      { label: 'Released', value: 'Jan 25, 2026' },
    ],
    screenshots: [
      '/screenshots/tabu-ekstra/1.jpg',
      '/screenshots/tabu-ekstra/2.jpg',
      '/screenshots/tabu-ekstra/3.jpg',
      '/screenshots/tabu-ekstra/4.jpg',
      '/screenshots/tabu-ekstra/5.jpg',
      '/screenshots/tabu-ekstra/6.jpg',
    ],
    meta: {
      version: '1.8.2',
      released: '2026-01-25',
      updated: '2026-07-02',
      minOS: 'iOS 15.6+',
      size: '37 MB',
      genre: 'Card · Word',
      rating: '4.5 / 5 (36 reviews)',
    },
  },
  {
    slug: 'imposter',
    name: 'Imposter',
    subtitle: 'Spy at the Party',
    tagline: 'A pass-and-play party word game with one liar in the room.',
    icon: '/icons/imposter.png',
    accent: '#d4a356',
    appStoreUrl: 'https://apps.apple.com/app/imposter-spy-at-the-party/id6761042851',
    short: 'Among Us / Spyfall-style party game. EN + TR localization.',
    about: [
      "A fast party word game where everyone knows the secret except the imposter.",
      "Pass the phone, reveal your role, and start the round. Most players see the same secret word — one player has to fake it. Give clues that help your group but stay subtle. Listen closely, spot weak answers, and vote before the imposter escapes suspicion.",
    ],
    features: [
      'Quick rounds for parties, hangouts, and family nights',
      'Pass-and-play setup — no second device needed',
      'Groups of 3 to 8 (Premium unlocks larger groups)',
      'Secret roles, clue giving, bluffing, voting',
      'Multiple categories and modes',
    ],
    techChips: ['Swift 5', 'SwiftUI', 'StoreKit 2', 'Google AdMob', 'RevenueCat', 'ATT', 'iOS 17.6+'],
    stack: [
      { label: 'Language', value: 'Swift 5' },
      { label: 'UI', value: 'SwiftUI' },
      { label: 'Monetization', value: 'Google AdMob + RevenueCat-managed StoreKit 2 (Imposter Premium)' },
      { label: 'Localization', value: 'English · Turkish' },
      { label: 'Privacy', value: 'ATT compliant' },
      { label: 'Min iOS', value: '17.6' },
    ],
    builtStory: [
      "A pass-and-play party game built entirely in SwiftUI, targeting iOS 17.6+ to lean on the latest navigation and animation APIs. The whole experience runs on a single device cycling through 3–8 players — no networking, no accounts, no friction.",
      "The trickiest UX problem was the secret-reveal moment: each player has to see their role privately, then hand the phone over. I built a press-and-hold reveal panel with a blur overlay that auto-locks the moment a finger lifts, so a glance from another player can't leak the role. State for roles, categories, and voting all lives in observable view models.",
      "All designs were made by me in Figma with help from AI tools.",
    ],
    stats: [
      { label: 'Released', value: 'May 2026' },
      { label: 'Players', value: '3–8' },
      { label: 'Localization', value: 'EN · TR' },
    ],
    screenshots: [
      '/screenshots/imposter/1.jpg',
      '/screenshots/imposter/2.jpg',
      '/screenshots/imposter/3.jpg',
      '/screenshots/imposter/4.jpg',
      '/screenshots/imposter/5.jpg',
    ],
    meta: {
      version: '0.4.1',
      released: '2026-05-03',
      updated: '2026-05-11',
      minOS: 'iOS 17.6+',
      size: '80 MB',
      genre: 'Party · Casual',
    },
  },
  {
    slug: 'holy-shift',
    name: 'Holy Shift',
    subtitle: 'Cyber Reflex Game',
    tagline: 'A high-speed cyberpunk reflex game with neon visuals.',
    icon: '/icons/holy-shift.png',
    accent: '#ff10b4',
    appStoreUrl: 'https://apps.apple.com/app/holy-shift-cyber-reflex-game/id6755365901',
    short: 'High-intensity arcade reflex game with a cyberpunk visual identity.',
    about: [
      "Can you survive the shift? Holy Shift is a high-speed, cyberpunk reflex game that tests your focus and reaction time.",
      "The rules are simple: tap to shift your color, match incoming orbs, survive as long as you can. But don't get comfortable — the system is unstable.",
    ],
    features: [
      'RIFT anomaly: survive sudden high-speed chaos bursts',
      'SHIELD & STRIKE: charge your multiplier under pressure',
      'Hyper-casual addiction loop — easy to learn, hard to master',
      'Cyberpunk aesthetic with neon visuals and glitch effects',
      'Customization: 6+ unlockable skins via in-game sparks',
      'High-score chaser against yourself and friends',
    ],
    techChips: ['Unity 2022 LTS', 'C#', 'Custom Shaders', 'Unity Ads', 'Google AdMob', 'Firebase', 'iOS 15.6+'],
    stack: [
      { label: 'Engine', value: 'Unity 2022 LTS' },
      { label: 'Language', value: 'C#' },
      { label: 'Visuals', value: 'Custom shaders, post-processing, glitch effects' },
      { label: 'Economy', value: 'In-game sparks currency, shop, skin unlocks' },
      { label: 'Monetization', value: 'Unity Ads + Google AdMob' },
      { label: 'Analytics', value: 'Google Analytics for Firebase' },
      { label: 'Min iOS', value: '15.6' },
    ],
    builtStory: [
      "A reflex arcade built in Unity 2022 LTS with C#. The visual identity — neon cyberpunk plus aggressive glitch effects — is driven by custom URP shaders and a post-processing chain. The core loop uses deterministic spawn timing so high scores are comparable across runs.",
      "Each-run difficulty is modulated by 'anomaly' events: RIFT bursts speed the spawn rate temporarily, while SHIELD/STRIKE windows let players bank multipliers under pressure. Players earn 'sparks' to unlock 6+ skins from an in-game shop. Monetization is Unity Ads + AdMob interstitials.",
      "All coding was done by me, and the visual assets were created in Procreate with help from AI tools. This project taught me a lot about hyper-casual mechanics and the process of fully developing a game, from the initial idea all the way to the App Store.",
    ],
    highlights: [
      '5 / 5 average rating',
    ],
    stats: [
      { label: 'Rating', value: '5.0 ★' },
      { label: 'Unlockables', value: '6+ skins' },
    ],
    previewVideoHls: 'https://apptrailers.itunes.apple.com/itunes-assets/PurpleVideo211/v4/8d/6a/16/8d6a16e9-f7b4-0bc0-4c12-bc12757bb91b/P1241418578_default.m3u8',
    previewVideoPoster: '/screenshots/holy-shift/1.jpg',
    screenshots: [
      '/screenshots/holy-shift/1.jpg',
      '/screenshots/holy-shift/2.jpg',
      '/screenshots/holy-shift/3.jpg',
      '/screenshots/holy-shift/4.jpg',
    ],
    meta: {
      version: '2.4',
      released: '2025-12-04',
      updated: '2026-01-18',
      minOS: 'iOS 15.6+',
      size: '152 MB',
      genre: 'Arcade · Reflex',
      rating: '5.0 / 5',
    },
  },
];

export function findApp(slug: string): AppData | undefined {
  return apps.find((a) => a.slug === slug);
}
