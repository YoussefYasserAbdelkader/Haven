export async function sendMessage(userMessage) {
  const response = await fetch('http://localhost:8000/message', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: userMessage })
  });

  if (!response.ok) throw new Error('Failed to send message');

  const data = await response.json();
  return data;
}
