#!/bin/bash
# deployment script for the chatbot application

echo "🚀 Preparing for deployment..."

# Navigate to frontend directory
cd chatbot-frontend

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Generate Prisma client
echo "🗄️ Generating Prisma client..."
npx prisma generate

# Build the application
echo "🔨 Building application..."
npm run build

echo "✅ Build completed successfully!"
echo "🌐 Ready for Vercel deployment!"