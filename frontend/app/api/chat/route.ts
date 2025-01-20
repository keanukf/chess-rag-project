import { NextResponse } from 'next/server'

export async function POST(req: Request) {
  const { question } = await req.json()

  try {
    const response = await fetch('http://192.168.178.173:8080/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: question }),
    })

    if (!response.ok) {
      throw new Error('Failed to get response from Flask backend')
    }

    const data = await response.json()
    console.log('Data received from backend:', data);
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error:', error)
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 })
  }
}

