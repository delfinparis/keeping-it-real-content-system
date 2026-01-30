import Link from "next/link";

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="md:col-span-2">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-gradient-to-br from-kale to-emerald-600 rounded-xl flex items-center justify-center">
                <span className="text-white font-bold text-lg">UA</span>
              </div>
              <span className="font-semibold text-lg">Unstuck Agent</span>
            </div>
            <p className="text-gray-400 text-sm leading-relaxed max-w-md">
              Get unstuck with advice from 500+ top producing real estate agents.
              Powered by the Keeping It Real podcast with D.J. Paris.
            </p>
            <div className="flex space-x-4 mt-4">
              <a
                href="https://www.keepingitrealpod.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-white transition"
                aria-label="Website"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                </svg>
              </a>
              <a
                href="https://open.spotify.com/show/6lDHbQ8nfuV87QyqiELilc"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-green-400 transition"
                aria-label="Spotify"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>
                </svg>
              </a>
              <a
                href="https://podcasts.apple.com/us/podcast/keeping-it-real-podcast-with-d-j-paris/id1031016891"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-purple-400 transition"
                aria-label="Apple Podcasts"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M5.34 0A5.328 5.328 0 000 5.34v13.32A5.328 5.328 0 005.34 24h13.32A5.328 5.328 0 0024 18.66V5.34A5.328 5.328 0 0018.66 0H5.34zm6.525 2.568c2.336 0 4.448.902 6.056 2.587 1.608 1.685 2.56 4.028 2.607 6.34a.103.103 0 01-.103.106h-1.818a.103.103 0 01-.103-.099c-.04-1.846-.817-3.527-2.12-4.727-1.303-1.2-2.99-1.86-4.519-1.86-1.53 0-3.217.66-4.52 1.86-1.303 1.2-2.08 2.881-2.12 4.727a.103.103 0 01-.102.099H3.264a.103.103 0 01-.103-.106c.047-2.312.999-4.655 2.607-6.34 1.608-1.685 3.72-2.587 6.056-2.587h.04zm.063 3.848c1.405 0 2.642.508 3.551 1.399.909.89 1.478 2.198 1.52 3.64a.103.103 0 01-.103.106h-1.818a.103.103 0 01-.102-.095c-.028-.902-.378-1.693-.956-2.26-.578-.568-1.306-.858-2.092-.858-.786 0-1.514.29-2.092.858-.578.567-.928 1.358-.956 2.26a.103.103 0 01-.103.095H6.918a.103.103 0 01-.103-.106c.042-1.442.611-2.75 1.52-3.64.909-.891 2.146-1.4 3.551-1.4h.04zm-.02 4.095c.975 0 1.765.79 1.765 1.765v5.478c0 .975-.79 1.765-1.765 1.765s-1.765-.79-1.765-1.765v-5.478c0-.975.79-1.765 1.765-1.765z"/>
                </svg>
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-semibold text-sm uppercase tracking-wider text-gray-400 mb-4">
              Get Unstuck
            </h3>
            <ul className="space-y-2">
              <li>
                <Link href="/" className="text-gray-300 hover:text-white transition text-sm">
                  Find Your Solution
                </Link>
              </li>
              <li>
                <Link href="/problems" className="text-gray-300 hover:text-white transition text-sm">
                  Browse by Problem
                </Link>
              </li>
              <li>
                <Link href="/episodes" className="text-gray-300 hover:text-white transition text-sm">
                  All Episodes
                </Link>
              </li>
            </ul>
          </div>

          {/* About */}
          <div>
            <h3 className="font-semibold text-sm uppercase tracking-wider text-gray-400 mb-4">
              The Podcast
            </h3>
            <ul className="space-y-2">
              <li>
                <a
                  href="https://www.keepingitrealpod.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-300 hover:text-white transition text-sm"
                >
                  Keeping It Real
                </a>
              </li>
              <li>
                <a
                  href="https://www.kalerealty.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-300 hover:text-white transition text-sm"
                >
                  Kale Realty
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Stats Bar */}
        <div className="border-t border-gray-800 mt-8 pt-8">
          <div className="flex flex-wrap justify-center gap-8 mb-6 text-center">
            <div>
              <p className="text-2xl font-bold text-kale">1,400+</p>
              <p className="text-xs text-gray-400 uppercase tracking-wide">Problems Identified</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-kale">950+</p>
              <p className="text-xs text-gray-400 uppercase tracking-wide">Clip Moments</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-kale">595</p>
              <p className="text-xs text-gray-400 uppercase tracking-wide">Episodes Analyzed</p>
            </div>
          </div>
          <div className="text-center text-gray-500 text-sm">
            <p>Powered by the Keeping It Real Podcast</p>
            <p className="mt-1">D.J. Paris · Kale Realty · Chicago</p>
          </div>
        </div>
      </div>
    </footer>
  );
}
