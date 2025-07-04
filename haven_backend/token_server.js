import express from 'express';
import { AccessToken } from 'livekit-server-sdk';

const app = express();
const port = 3000;

const LIVEKIT_API_KEY = 'APIhJtwYGLDmsi5';
const LIVEKIT_API_SECRET = 'eJj3BoKCIKscDW7OYwFFVoTB8XAVnLxXxe56sIGthJU';

app.get('/token', (req, res) => {
  const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
    identity: 'user_' + Math.floor(Math.random() * 1000),
  });

  token.addGrant({ roomJoin: true, room: 'haven' });

  res.json({ token: token.toJwt() });
});

app.listen(port, () => {
  console.log(`Token server running on http://localhost:${port}`);
});
