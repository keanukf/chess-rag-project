'use client'

import { useState } from 'react'
import { ArrowUpIcon } from 'lucide-react'
import { Message } from './Message'

interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
}

const suggestions = [
  "Who won the most games on chess.com in 2024?",
  "What was the highest rated game in 2024?"
]

export function Chat() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value)
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    await sendMessage(input)
  }

  const sendMessage = async (message: string) => {
    if (!message.trim() || isLoading) return

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: message
    }

    setMessages(prevMessages => [...prevMessages, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: message }),
      })

      if (!response.ok) {
        throw new Error('Failed to get response from the server')
      }

      const data = await response.json()
      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.answer
      }

      setMessages(prevMessages => [...prevMessages, assistantMessage])
    } catch (error) {
      console.error('Error:', error)
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, there was an error processing your request. Please try again.'
      }
      setMessages(prevMessages => [...prevMessages, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleSuggestionClick = (suggestion: string) => {
    sendMessage(suggestion)
  }

  return (
    <div className="flex flex-col h-[90vh] w-96 mx-auto bg-white rounded-3xl shadow-lg overflow-hidden">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <Message key={message.id} message={message} />
        ))}
      </div>
      <div className="p-4 border-t space-y-4">
        <div className="flex space-x-2">
          {suggestions.map((suggestion, index) => (
            <button
              key={index}
              onClick={() => handleSuggestionClick(suggestion)}
              className="flex-1 p-2 bg-gray-100 text-sm text-gray-700 rounded-lg hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
            >
              {suggestion}
            </button>
          ))}
        </div>
        <form onSubmit={handleSubmit} className="relative">
          <input
            type="text"
            value={input}
            onChange={handleInputChange}
            placeholder="Ask about chess.com games in 2024..."
            className="w-full p-3 pr-12 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="absolute right-2 top-1/2 transform -translate-y-1/2 p-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
          >
            {isLoading ? (
              <div className="w-5 h-5 border-t-2 border-white rounded-full animate-spin"></div>
            ) : (
              <ArrowUpIcon className="w-5 h-5" />
            )}
          </button>
        </form>
      </div>
    </div>
  )
}

