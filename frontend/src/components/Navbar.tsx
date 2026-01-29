'use client';

import { FaBrain } from 'react-icons/fa';

export default function Navbar() {
  const scrollToSection = (id: string) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <nav className="fixed w-full top-0 z-50 h-[70px] flex items-center justify-between px-[5%] bg-[#050510]/70 backdrop-blur-md border-b border-white/5">
      <div className="flex items-center gap-2">
        <div className="w-[35px] h-[35px] rounded-lg bg-gradient-to-br from-[#00f2ff] to-[#00a8ff] flex items-center justify-center font-bold text-black shadow-[0_0_15px_rgba(0,242,255,0.4)]">
          C
        </div>
        <span className="text-xl font-semibold tracking-wide text-white">
          CODDY <span className="font-light text-[#00f2ff]">AI</span>
        </span>
      </div>

      <div className="flex gap-8 text-sm font-medium">
        <button onClick={() => scrollToSection('home')} className="text-[#a0a0a0] hover:text-white hover:text-shadow-glow transition-all">
          Home
        </button>
        <button onClick={() => scrollToSection('features')} className="text-[#a0a0a0] hover:text-white hover:text-shadow-glow transition-all">
          Capabilities
        </button>
        <button onClick={() => scrollToSection('ai-core')} className="text-[#00f2ff] hover:text-white hover:shadow-[0_0_10px_#00f2ff] transition-all">
          Neural Core
        </button>
      </div>
    </nav>
  );
}
