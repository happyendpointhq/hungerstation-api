// HungerStation API quickstart. Node 18+ (built-in fetch), no dependencies.
//   RAPIDAPI_KEY=... node quickstart.mjs

const HOST = 'hungerstation1.p.rapidapi.com';

async function get(path, params = {}) {
  const url = new URL(`https://${HOST}${path}`);
  for (const [key, value] of Object.entries(params)) {
    if (value != null) url.searchParams.set(key, value);
  }
  const res = await fetch(url, {
    headers: { 'x-rapidapi-host': HOST, 'x-rapidapi-key': process.env.RAPIDAPI_KEY },
  });
  if (!res.ok) throw new Error(`HungerStation API ${res.status}: ${await res.text()}`);
  return (await res.json()).data;
}

// Restaurants delivering to a point in north Riyadh, best rated first.
const data = await get('/restaurants-nearby', {
  latitude: 24.81338091423363,
  longitude: 46.70321613550186,
  sort: 'rating',
  limit: 10,
  language: 'en',
});
console.log(`${data.total_count} vendors deliver here`);
for (const v of data.vendors) {
  const ad = v.sponsored ? ' [ad]' : '';
  console.log(
    `${String(v.rating).padStart(4)} (${v.rating_count})  ${v.eta_min}-${v.eta_max} min  ${v.delivery_fee} SAR  ${v.name}${ad}`
  );
}
