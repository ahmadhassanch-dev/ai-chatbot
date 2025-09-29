# AI Chatbot Full Stack Application

A professional full-stack AI chatbot application built with Next.js, FastAPI, and Gemini AI.

## 🚀 Features

### Frontend (Next.js)
- **Beautiful Landing Page** with modern animations using Framer Motion
- **User Authentication** with NextAuth.js (Sign up/Sign in)
- **Professional Chat Interface** with real-time messaging
- **Responsive Design** optimized for all devices
- **Modern UI Components** using Radix UI and Tailwind CSS
- **User Profiles** and session management
- **Smooth Animations** with Framer Motion

### Backend (Python/FastAPI)
- **AI Agent Framework** using OpenAI SDK with Gemini API
- **Professional Agent Architecture** with Agent, Runner, and Model classes
- **REST API** with FastAPI for frontend integration
- **CORS Support** for web applications
- **Environment Configuration** for secure API key management
- **Error Handling** and logging

### Database & Authentication
- **SQLite Database** with Prisma ORM
- **User Management** with secure password hashing
- **Session Management** with NextAuth.js
- **Chat History** storage (ready for implementation)

## 🛠 Technology Stack

**Frontend:**
- Next.js 15 (App Router)
- TypeScript
- Tailwind CSS
- Radix UI Components
- Framer Motion
- NextAuth.js
- Prisma ORM
- Axios

**Backend:**
- Python 3.13
- FastAPI
- OpenAI SDK
- Gemini AI API
- Uvicorn

**Database:**
- SQLite (development)
- Prisma ORM

## 📦 Installation & Setup

### Frontend Setup
```bash
cd chatbot-frontend
npm install
npx prisma generate
npx prisma db push
npm run dev
```

### Backend Setup
```bash
cd chatbot-backend
pip install -r requirements.txt
python api_server.py
```

### Environment Variables

**Frontend (.env):**
```
DATABASE_URL="file:./dev.db"
NEXTAUTH_SECRET="your-nextauth-secret"
NEXTAUTH_URL="http://localhost:3000"
NEXT_PUBLIC_API_URL="http://localhost:8000"
```

**Backend (.env):**
```
GEMINI_API_KEY="AIzaSyCVw0fs416KvQ7WDd-LpbKQs0tPz29g5S4"
GEMINI_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
GEMINI_MODEL="gemini-2.5-flash"
PORT=8000
HOST=0.0.0.0
```

## 🎨 UI Components

### Landing Page
- Hero section with animated gradient backgrounds
- Feature cards with hover effects
- Call-to-action sections
- Responsive navigation header
- Professional footer

### Authentication Pages
- Modern sign-up/sign-in forms
- Input validation with Zod
- Password visibility toggle
- Loading states and error handling
- Success animations

### Chat Interface
- Real-time messaging interface
- Sidebar with chat history
- User profile management
- Typing indicators
- Message timestamps
- Responsive design

## 🚀 Deployment Instructions

### Vercel Deployment (Frontend)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy on Vercel:**
   - Connect your GitHub repository
   - Set environment variables in Vercel dashboard
   - Deploy automatically

3. **Environment Variables for Production:**
   ```
   DATABASE_URL="your-production-database-url"
   NEXTAUTH_SECRET="your-secure-secret"
   NEXTAUTH_URL="https://your-domain.vercel.app"
   NEXT_PUBLIC_API_URL="https://your-backend-url"
   ```

### Backend Deployment Options

1. **Railway/Render:**
   - Push backend to separate repository
   - Configure environment variables
   - Deploy Python application

2. **Vercel Serverless Functions:**
   - Move API routes to Next.js API routes
   - Convert Python backend to Node.js

## 📱 Features Overview

### 🔐 Authentication System
- User registration and login
- Secure password hashing with bcrypt
- JWT session management
- Protected routes

### 💬 Chat System
- Real-time AI conversations
- Message history
- Multiple agent types (Basic, Creative, Technical, Customer Support)
- Typing indicators

### 🎨 Modern UI
- Gradient backgrounds and animations
- Responsive design
- Dark/light mode ready
- Professional color scheme
- Smooth transitions

### 🤖 AI Integration
- Gemini 2.5 Flash AI model
- Intelligent conversation handling
- Context-aware responses
- Error handling for API failures

## 🔧 Development Commands

**Frontend:**
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Lint code
```

**Backend:**
```bash
python api_server.py # Start API server
python chatbot_core.py # Test core functionality
```

## 📊 API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /agent-info` - Agent information
- `POST /chat` - Send message to AI
- `POST /api/auth/signup` - User registration
- `POST /api/auth/[...nextauth]` - Authentication

## 🎯 Ready for Production

The application is fully configured for deployment with:
- Environment variable management
- Database migrations
- Error handling
- Security best practices
- CORS configuration
- Professional UI/UX

Deploy to Vercel with zero configuration changes needed!