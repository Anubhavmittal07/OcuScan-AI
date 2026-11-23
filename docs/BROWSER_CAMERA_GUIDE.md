# WebRTC Camera Permission & Device Compatibility Notes

When running EyeHealthAI in clinical screening environments, several browser security behaviors apply:

### 1. HTTPS vs Localhost
- Modern browsers (Chrome 80+, Safari 14+) require a secure origin (`https://` or `http://localhost`) to grant getUserMedia permissions.
- In intranet hospital setups, configure reverse proxy with self-signed or enterprise TLS certs.

### 2. Mobile Macro Focus
- On smartphone browsers, the primary wide lens typically offers better close-up focus on the palpebral conjunctiva than ultra-wide lenses.
- We recommend positioning the camera 10–15 cm from the eye under soft diffuse room lighting.
