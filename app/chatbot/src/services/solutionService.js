const API_TIMEOUT_MS = 10000;

export const fetchMatchingSolution = async({ product, reason, reasonType, partnerId }) => {
  const params = new URLSearchParams({
    product,
    reason,
    reasonType,
    partnerId,
  });

  const controller = new AbortController();
  const tid = setTimeout(() => controller.abort(), API_TIMEOUT_MS);

  try {
    const res = await fetch(`/recommend?${params.toString()}`, {
      method: 'GET',
      signal: controller.signal,
    });


    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const text = await res.text();
    try {
      const data = JSON.parse(text);
      return data.solution ?? text;
    } catch {
      return text;
    }
  } finally {
    clearTimeout(tid);
  }
}



