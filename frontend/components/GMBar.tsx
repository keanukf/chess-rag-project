import Image from 'next/image'
import Link from 'next/link'

const GMs = [
  { name: 'Magnus Carlsen', image: '/images/magnus-carlsen.jpeg', link: 'https://www.chess.com/member/magnuscarlsen' },
  { name: 'Hikaru Nakamura', image: '/images/hikaru-nakamura.jpeg', link: 'https://www.chess.com/member/hikaru' },
  { name: 'Fabiano Caruana', image: '/images/fabiano-caruana.jpeg', link: 'https://www.chess.com/member/fabianocaruana' },
  { name: 'Ian Nepomniachtchi', image: '/images/ian-nepomniachtchi.jpeg', link: 'https://www.chess.com/member/lachesisq' },
  { name: 'Alireza Firouzja', image: '/images/alireza-firouzja.jpeg', link: 'https://www.chess.com/member/firouzja2003' },
  { name: 'Wesley So', image: '/images/wesley-so.jpeg', link: 'https://www.chess.com/member/gmwso' },
]

export function GMBar() {
  return (
    <div className="flex flex-col items-center space-y-6 bg-white rounded-full py-6 px-3 shadow-lg">
      {GMs.map((gm, index) => (
        <div key={index} className="relative group">
          <Link href={gm.link} target="_blank" rel="noopener noreferrer">
            <div className="transition-all duration-300 ease-in-out transform group-hover:scale-125 z-10">
              <Image
                src={gm.image || "/placeholder.svg"}
                alt={gm.name}
                width={50}
                height={50}
              className="rounded-full"
              />
            </div>
          </Link>
          <span className="absolute left-1/2 transform -translate-x-1/2 mt-2 px-3 py-1 bg-gray-800 text-white text-xs rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap z-20">
            {gm.name}
          </span>
        </div>
      ))}
    </div>
  )
}

