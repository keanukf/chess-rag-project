import { Chat } from '../components/Chat'
import { GMBar } from '../components/GMBar'

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-100 flex items-center justify-center p-8">
      <div className="flex items-start space-x-4">
        <GMBar />
        <Chat />
      </div>
    </main>
  )
}

