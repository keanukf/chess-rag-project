import { Chat } from "../components/Chat"
import { GMBar } from "../components/GMBar"

export default function Home() {
  return (
    <main className="min-h-screen h-screen bg-gray-100 flex flex-col justify-between">
      <header className="absolute top-0 left-0 p-4">
        <img src="/images/chessbot.png" alt="Chessbot Logo" className="h-12 w-auto" />
      </header>
      <div className="flex items-start justify-center space-x-0 p-4 flex-1 overflow-hidden">
        <div className="flex justify-center w-full pb-4">
          <Chat />
        </div>
      </div>
      <div className="fixed right-4 top-1/2 transform -translate-y-1/2">
        <GMBar />
      </div>
      <footer className="w-full bg-transparent">
        <div className="max-w-7xl mx-auto py-2">
          <p className="text-center text-xs text-gray-400">
            This chatbot provides information based on chess.com game results from 2024 for specific players. The accuracy of the
            information is subject to the data available. Player images are from chess.com. All image rights reserved by chess.com.
          </p>
        </div>
      </footer>
    </main>
  )
}

