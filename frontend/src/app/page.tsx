'use client';

import Navbar from '@/components/Navbar';
import ChatInterface from '@/components/ChatInterface';
import { motion } from 'framer-motion';
import { FaPython, FaJs, FaReact, FaJava, FaRust, FaMicrochip } from 'react-icons/fa';
import { SiCplusplus, SiTypescript, SiDocker } from 'react-icons/si';

// Data for capabilities
const features = [
  { icon: FaPython, name: 'Python', desc: 'Data Science & Neural Networks', color: '#306998' },
  { icon: SiTypescript, name: 'TypeScript', desc: 'Type-Safe Web Architecture', color: '#3178C6' },
  { icon: SiCplusplus, name: 'C++', desc: 'High-Performance Systems', color: '#00599C' },
  { icon: FaReact, name: 'React', desc: 'Modern Reactive UI', color: '#61DAFB' },
  { icon: SiDocker, name: 'Docker', desc: 'Containerized Deployment', color: '#2496ED' },
  { icon: FaRust, name: 'Rust', desc: 'Memory-Safe Engineering', color: '#DEA584' },
];

export default function Home() {
  return (
    <div className="bg-[#050510] min-h-screen text-white overflow-x-hidden relative">
      <Navbar />

      {/* GLOBAL AMBIENT LIGHT */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none z-0">
        <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-[#00f2ff] rounded-full blur-[150px] opacity-10" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[600px] h-[600px] bg-[#ff00ff] rounded-full blur-[180px] opacity-10" />
      </div>

      {/* HERO SECTION */}
      <section id="home" className="min-h-screen flex flex-col items-center justify-center relative z-10 pt-20">
        <div className="text-center max-w-5xl px-6">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8 }}
          >
            <div className="inline-flex items-center gap-2 px-4 py-1.5 mb-8 rounded-full border border-[#00f2ff]/30 bg-[#00f2ff]/5 text-[#00f2ff] text-xs font-bold tracking-[0.2em] uppercase shadow-[0_0_20px_rgba(0,242,255,0.1)]">
              <span className="w-2 h-2 rounded-full bg-[#00f2ff] animate-pulse" />
              System Online v2.1
            </div>
            
            <h1 className="text-6xl md:text-9xl font-bold mb-6 tracking-tighter leading-tight">
              NEURAL <br />
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-[#00f2ff] via-[#ffffff] to-[#00a8ff] drop-shadow-[0_0_30px_rgba(0,242,255,0.3)]">
                ARCHITECT
              </span>
            </h1>
            
            <p className="text-lg md:text-2xl text-[#a0a0a0] mb-12 max-w-3xl mx-auto font-light leading-relaxed">
              Your premium local AI companion. <br/>
              Engineered by <strong className="text-white">Biagio Scaglia</strong> for superior coding workflows.
            </p>
          </motion.div>

          <motion.button
            whileHover={{ scale: 1.05, boxShadow: "0 0 40px rgba(0, 242, 255, 0.4)" }}
            whileTap={{ scale: 0.95 }}
            onClick={() => document.getElementById('ai-core')?.scrollIntoView({ behavior: 'smooth' })}
            className="px-10 py-4 bg-white text-black font-bold rounded-full text-lg transition-all"
          >
            INITIALIZE SESSION
          </motion.button>
        </div>
      </section>

      {/* WHY CODDY SECTION */}
      <section className="py-20 relative z-10">
        <div className="max-w-6xl mx-auto px-6 grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
                { title: "Privacy First", desc: "100% Local execution. Your code never leaves your machine." },
                { title: "Latency Zero", desc: "Optimized for speed with local neural inference engines." },
                { title: "Context Aware", desc: "Deep understanding of your project structure and dependencies." }
            ].map((item, i) => (
                <div key={i} className="glass p-6 rounded-2xl border border-white/5 bg-white/5 backdrop-blur-sm">
                    <h3 className="text-[#00f2ff] font-bold mb-2 text-lg">{item.title}</h3>
                    <p className="text-[#a0a0a0] text-sm leading-relaxed">{item.desc}</p>
                </div>
            ))}
        </div>
      </section>

      {/* CAPABILITIES SECTION */}
      <section id="features" className="py-32 relative z-10 px-6">
        <div className="max-w-7xl mx-auto">
          <motion.div 
             initial={{ opacity: 0, y: 20 }}
             whileInView={{ opacity: 1, y: 0 }}
             viewport={{ once: true }}
             className="mb-16 text-center"
          >
            <h2 className="text-4xl font-bold mb-4 tracking-tight">Polyglot Mastery</h2>
            <div className="h-1 w-20 bg-gradient-to-r from-[#00f2ff] to-transparent mx-auto rounded-full" />
          </motion.div>

          {/* GRID LAYOUT FIX */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-50px" }}
                transition={{ delay: idx * 0.1 }}
                whileHover={{ y: -10 }}
                className="group relative p-8 rounded-3xl border border-white/5 bg-[#0a0a16]/80 backdrop-blur-xl hover:bg-[#1a1a2e] transition-all duration-300 overflow-hidden"
              >
                {/* Hover Glow Effect */}
                <div 
                  className="absolute inset-0 opacity-0 group-hover:opacity-20 transition-opacity duration-500 pointer-events-none" 
                  style={{ background: `radial-gradient(circle at center, ${feature.color}, transparent 70%)` }}
                />

                <div className="relative z-10 flex flex-col items-center text-center">
                  <div 
                    className="mb-6 p-5 rounded-2xl bg-white/5 border border-white/10 group-hover:border-white/20 transition-colors"
                  >
                    <feature.icon size={40} color={feature.color} />
                  </div>
                  
                  <h3 className="text-2xl font-bold mb-3">{feature.name}</h3>
                  <p className="text-[#888] text-sm font-medium">{feature.desc}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* AI CORE SECTION */}
      <section id="ai-core" className="min-h-screen py-20 px-4 flex flex-col items-center relative z-10">
        <div className="w-full max-w-[1400px]">
          <div className="flex items-center justify-between mb-8 px-4">
             <div className="flex items-center gap-4">
                <div className="p-3 bg-[#00f2ff]/10 rounded-xl border border-[#00f2ff]/20">
                   <FaMicrochip size={24} className="text-[#00f2ff]" />
                </div>
                <div>
                   <h2 className="text-2xl font-bold text-white tracking-wide">Neural Core</h2>
                   <p className="text-[#666] text-xs uppercase tracking-wide">Connected via Localhost:8000</p>
                </div>
             </div>
          </div>
          
          <ChatInterface />
        </div>
      </section>

      {/* FOOTER */}
      <footer className="py-10 text-center border-t border-white/5 bg-[#020205] relative z-10">
        <p className="text-[#444] text-sm">
          Developed by <span className="text-[#fff] font-medium">Biagio Scaglia</span>
        </p>
      </footer>
    </div>
  );
}
