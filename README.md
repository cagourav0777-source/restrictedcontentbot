# Telegram Bot Cloner

A Telegram bot that creates content saver bots for public channels.

## Features
- 1-Click Bot Cloning (forward bot tokens or paste manually)
- Redis Database for persistence
- Seamless Content Forwarding from public channels

## Deployment

### 1. Get Credentials
- API ID/Hash from [my.telegram.org](https://my.telegram.org)
- Bot Token from [@BotFather](https://t.me/BotFather) (`/newbot` command)
- Redis credentials from [Upstash](https://upstash.com) (free tier available)

### 2. Configure Environment
```bash
git clone https://github.com/Harshit-shrivastav/Save-Contents-Cloner-Bot.git
cd Save-Contents-Cloner-Bot
pip install -r requirements.txt
```

Create `.env` file:
```env
API_ID=1234567
API_HASH=your_api_hash_here
BOT_TOKEN=123:your_bot_token
AUTH_USER_ID=your_telegram_id
REDIS_HOST=your_redis_host
REDIS_PORT=your_redis_port
REDIS_PASSWORD=your_redis_password
```

### 3. Launch Your Bot
```bash
python3 -m main
```

## Cloud Deployment

### Deploy on Render
1. Fork this repository
2. Go to [render.com](https://render.com) and create a new Web Service
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` configuration
5. Add environment variables in Render dashboard:
   - API_ID
   - API_HASH
   - BOT_TOKEN
   - AUTH_USER_ID
   - REDIS_HOST
   - REDIS_PORT
   - REDIS_PASSWORD
6. Deploy

### Deploy on Railway
1. Fork this repository
2. Go to [railway.app](https://railway.app) and create a new project
3. Select "Deploy from GitHub repo"
4. Railway will automatically detect the configuration
5. Add environment variables in Railway dashboard:
   - API_ID
   - API_HASH
   - BOT_TOKEN
   - AUTH_USER_ID
   - REDIS_HOST
   - REDIS_PORT
   - REDIS_PASSWORD
6. Deploy

## How to Clone Bots
1. Create new bot with [@BotFather](https://t.me/BotFather)
2. Copy the token (format: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)
3. Forward the message from @BotFather to your main bot

## License
MIT
