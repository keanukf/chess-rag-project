interface MessageProps {
  message: {
    role: 'user' | 'assistant'
    content: string
  }
}

export function Message({ message }: MessageProps) {
  return (
    <div
      className={`flex ${
        message.role === 'user' ? 'justify-end' : 'justify-start'
      }`}
    >
      <div
        className={`max-w-[80%] p-4 rounded-2xl ${
          message.role === 'user'
            ? 'bg-blue-500 text-white'
            : 'bg-gray-200 text-gray-800'
        }`}
      >
        <p>{message.content}</p>
      </div>
    </div>
  )
}

