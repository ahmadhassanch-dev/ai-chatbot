"use client"

import { useState, useEffect, useRef } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Send, Bot, User, Settings, Plus, MessageSquare, Sparkles, ArrowLeft } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Card, CardContent } from "@/components/ui/card"
import Link from "next/link"
import axios from "axios"

interface Message {
  id: string
  content: string
  role: "user" | "assistant"
  timestamp: Date
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      role: "user",
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMessage])
    setInput("")
    setIsLoading(true)
    setIsTyping(true)

    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/chat`,
        {
          message: input,
          agent_type: "basic"
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      )

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.data.response,
        role: "assistant",
        timestamp: new Date(),
      }

      setIsTyping(false)
      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error("Error sending message:", error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: "Sorry, I'm having trouble connecting. Please try again later.",
        role: "assistant",
        timestamp: new Date(),
      }
      setIsTyping(false)
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const startNewChat = () => {
    setMessages([])
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="flex h-screen">
        {/* Sidebar */}
        <motion.div
          initial={{ x: -300 }}
          animate={{ x: 0 }}
          className="w-64 bg-white/80 backdrop-blur-sm border-r border-gray-200 flex flex-col"
        >
          <div className="p-4 border-b border-gray-200">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                <Bot className="w-4 h-4 text-white" />
              </div>
              <div>
                <h1 className="font-bold text-lg bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  AI Assistant
                </h1>
              </div>
            </div>
            <Link href="/">
              <Button variant="outline" size="sm" className="w-full">
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to Home
              </Button>
            </Link>
          </div>

          <div className="flex-1 p-4">
            <Button
              variant="outline"
              className="w-full mb-4 border-dashed border-gray-300 hover:border-blue-500 hover:bg-blue-50"
              onClick={startNewChat}
            >
              <Plus className="w-4 h-4 mr-2" />
              New Chat
            </Button>

            <div className="space-y-2">
              <div className="flex items-center px-3 py-2 rounded-lg bg-blue-50 border border-blue-200">
                <MessageSquare className="w-4 h-4 text-blue-600 mr-3" />
                <span className="text-sm text-blue-800">Current Chat</span>
              </div>
            </div>
          </div>

          <div className="p-4 border-t border-gray-200">
            <div className="flex items-center space-x-3 mb-3">
              <Avatar className="h-8 w-8">
                <AvatarFallback className="bg-gradient-to-r from-green-500 to-blue-600 text-white">
                  <User className="w-4 h-4" />
                </AvatarFallback>
              </Avatar>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900">
                  Anonymous User
                </p>
                <p className="text-xs text-gray-500">
                  No login required
                </p>
              </div>
            </div>
            <Button variant="outline" size="sm" className="w-full">
              <Settings className="w-4 h-4 mr-2" />
              Settings
            </Button>
          </div>
        </motion.div>

        {/* Main Chat Area */}
        <div className="flex-1 flex flex-col">
          {/* Header */}
          <motion.div
            initial={{ y: -50 }}
            animate={{ y: 0 }}
            className="bg-white/80 backdrop-blur-sm border-b border-gray-200 p-4"
          >
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <div>
                <h2 className="font-semibold text-lg text-gray-900">AI Assistant</h2>
                <p className="text-sm text-gray-500">
                  {isTyping ? "Thinking..." : "Ready to help you"}
                </p>
              </div>
            </div>
          </motion.div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            <AnimatePresence>
              {messages.length === 0 ? (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="text-center py-12"
                >
                  <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Bot className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-800 mb-2">
                    Welcome to AI Assistant!
                  </h3>
                  <p className="text-gray-600 max-w-md mx-auto">
                    I&apos;m here to help you with questions, creative tasks, problem-solving, and more. 
                    What would you like to talk about today?
                  </p>
                </motion.div>
              ) : (
                messages.map((message, index) => (
                  <motion.div
                    key={message.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className={`flex space-x-3 ${
                      message.role === "user" ? "justify-end" : "justify-start"
                    }`}
                  >
                    {message.role === "assistant" && (
                      <Avatar className="h-8 w-8 mt-1">
                        <AvatarFallback className="bg-gradient-to-r from-blue-500 to-purple-600 text-white">
                          <Bot className="w-4 h-4" />
                        </AvatarFallback>
                      </Avatar>
                    )}
                    
                    <Card className={`max-w-xs lg:max-w-md xl:max-w-lg ${
                      message.role === "user" 
                        ? "bg-gradient-to-r from-blue-500 to-purple-600 text-white" 
                        : "bg-white/80 backdrop-blur-sm"
                    }`}>
                      <CardContent className="p-3">
                        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                        <p className={`text-xs mt-2 ${
                          message.role === "user" ? "text-blue-100" : "text-gray-500"
                        }`}>
                          {message.timestamp.toLocaleTimeString([], { 
                            hour: '2-digit', 
                            minute: '2-digit' 
                          })}
                        </p>
                      </CardContent>
                    </Card>

                    {message.role === "user" && (
                      <Avatar className="h-8 w-8 mt-1">
                        <AvatarFallback className="bg-gradient-to-r from-green-500 to-blue-600 text-white">
                          <User className="w-4 h-4" />
                        </AvatarFallback>
                      </Avatar>
                    )}
                  </motion.div>
                ))
              )}

              {isTyping && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="flex space-x-3 justify-start"
                >
                  <Avatar className="h-8 w-8 mt-1">
                    <AvatarFallback className="bg-gradient-to-r from-blue-500 to-purple-600 text-white">
                      <Bot className="w-4 h-4" />
                    </AvatarFallback>
                  </Avatar>
                  <Card className="bg-white/80 backdrop-blur-sm">
                    <CardContent className="p-3">
                      <div className="flex space-x-1">
                        <motion.div
                          animate={{ y: [0, -5, 0] }}
                          transition={{ duration: 1, repeat: Infinity, delay: 0 }}
                          className="w-2 h-2 bg-gray-400 rounded-full"
                        />
                        <motion.div
                          animate={{ y: [0, -5, 0] }}
                          transition={{ duration: 1, repeat: Infinity, delay: 0.2 }}
                          className="w-2 h-2 bg-gray-400 rounded-full"
                        />
                        <motion.div
                          animate={{ y: [0, -5, 0] }}
                          transition={{ duration: 1, repeat: Infinity, delay: 0.4 }}
                          className="w-2 h-2 bg-gray-400 rounded-full"
                        />
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              )}
            </AnimatePresence>
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <motion.div
            initial={{ y: 50 }}
            animate={{ y: 0 }}
            className="border-t border-gray-200 bg-white/80 backdrop-blur-sm p-4"
          >
            <form onSubmit={sendMessage} className="flex space-x-3">
              <div className="flex-1 relative">
                <Input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Type your message here..."
                  className="pr-12 border-gray-200 focus:border-blue-500 focus:ring-blue-500"
                  disabled={isLoading}
                />
              </div>
              <Button
                type="submit"
                disabled={isLoading || !input.trim()}
                className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white"
              >
                <Send className="w-4 h-4" />
              </Button>
            </form>
          </motion.div>
        </div>
      </div>
    </div>
  )
}