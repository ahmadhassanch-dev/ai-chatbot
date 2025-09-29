# AI Chatbot - Professional Full Stack Application

A modern AI chatbot with beautiful UI, user authentication, and Gemini AI integration.

## 🌟 Features

- **Beautiful Landing Page** with smooth animations
- **User Authentication** (Sign up/Sign in)
- **Real-time AI Chat** powered by Gemini 2.5 Flash
- **Professional UI** with modern design
- **Responsive Design** for all devices
- **Secure Database** with user management

## 🚀 Live Demo

[Live Application](https://your-app-name.vercel.app)

## 📱 Screenshots

![Landing Page](./screenshots/landing.png)
![Chat Interface](./screenshots/chat.png)

## 🛠 Technology Stack

- **Frontend:** Next.js 15, TypeScript, Tailwind CSS, Framer Motion
- **Backend:** Python FastAPI, OpenAI SDK, Gemini AI
- **Database:** SQLite with Prisma ORM
- **Authentication:** NextAuth.js
- **Deployment:** Vercel

## ⚡ Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-chatbot.git
cd ai-chatbot

# Frontend setup
cd chatbot-frontend
npm install
npx prisma generate
npx prisma db push
npm run dev

# Backend setup (separate terminal)
cd chatbot-backend  
pip install -r requirements.txt
python api_server.py
```

## 🌐 Environment Variables

Create `.env.local` in the frontend directory:

```env
DATABASE_URL="file:./dev.db"
NEXTAUTH_SECRET="your-secure-secret"
NEXTAUTH_URL="http://localhost:3000"
NEXT_PUBLIC_API_URL="http://localhost:8000"
```

## 📦 Deployment

The application is configured for one-click deployment on Vercel:

1. Push to GitHub
2. Connect to Vercel  
3. Add environment variables
4. Deploy automatically

## 🔧 Development

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
```

## 📄 License

MIT License - feel free to use this project for your own purposes!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

Built with ❤️ using Next.js and Gemini AI