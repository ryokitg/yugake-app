export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const { image, prompt } = req.body;
    if (!image || !prompt) return res.status(400).json({ error: 'missing params' });

    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': process.env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-5',
        max_tokens: 400,
        messages: [{ role: 'user', content: [
          { type: 'image', source: { type: 'base64', media_type: 'image/jpeg', data: image } },
          { type: 'text', text: prompt }
        ]}]
      })
    });

    const data = await response.json();
    if (!response.ok) return res.status(500).json({ error: data.error?.message || 'API error' });

    const raw = data.content.map(b => b.text || '').join('');
    const match = raw.match(/\{[^}]+\}/);
    if (!match) return res.status(500).json({ error: 'no JSON: ' + raw.substring(0, 80) });

    const parsed = JSON.parse(match[0]);
    return res.status(200).json({ result: parsed });

  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
}
