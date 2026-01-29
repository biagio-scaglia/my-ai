'use client';

import { useState, useRef, useEffect } from 'react';
import { FaPaperPlane, FaRobot, FaUser, FaTerminal, FaEraser } from 'react-icons/fa';
import { motion, AnimatePresence } from 'framer-motion';

type Message = {
  role: 'user' | 'assistant';
  content: string;
};

export default function ChatInterface() {
  const [mounted, setMounted] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: "Systems online.\nMemory Banks: ACTIVE\nNeural Engine: READY\n\nHow can I assist you today, Biagio?" }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  // Ref for the scroll container
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const [shouldAutoScroll, setShouldAutoScroll] = useState(true);

  // Check if we should stick to bottom on scroll
  const handleScroll = () => {
    if (!scrollContainerRef.current) return;
    const { scrollTop, scrollHeight, clientHeight } = scrollContainerRef.current;
    // If user is within 100px of bottom, auto-scroll is ON
    const isAtBottom = scrollHeight - scrollTop - clientHeight < 100;
    setShouldAutoScroll(isAtBottom);
  };

  const scrollToBottom = () => {
    if (shouldAutoScroll) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, shouldAutoScroll]);

  const clearChat = () => {
      setMessages([{ role: 'assistant', content: "History cleared. Ready for new tasks." }]);
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setShouldAutoScroll(true); // Force scroll on new message

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: [...messages, userMessage],
          use_web: false
        })
      });

      if (!response.body) throw new Error("No response body");

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let aiContent = '';
      
      setMessages(prev => [...prev, { role: 'assistant', content: '' }]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        aiContent += chunk;
        
        setMessages(prev => {
          const newMessages = [...prev];
          newMessages[newMessages.length - 1].content = aiContent;
          return newMessages;
        });
      }

    } catch (error) {
      console.error("Chat error:", error);
      setMessages(prev => [...prev, { role: 'assistant', content: "Error: Could not connect to Neural Core. Ensure backend is running." }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };



  return (
    <div className="w-full h-[750px] flex flex-col relative rounded-3xl overflow-hidden border border-white/10 bg-[#0c0c16]/50 backdrop-blur-2xl shadow-[0_0_50px_rgba(0,0,0,0.5)]">
      
      {/* HEADER */}
      <div className="h-14 px-6 border-b border-white/5 bg-white/5 flex items-center justify-between">
         <div className="flex items-center gap-3">
             <div className="flex gap-2">
                 <div className="w-3 h-3 rounded-full bg-red-500/50" />
                 <div className="w-3 h-3 rounded-full bg-yellow-500/50" />
                 <div className="w-3 h-3 rounded-full bg-green-500/50" />
             </div>
             <span className="ml-4 font-mono text-xs text-[#666]">user@coddy-ai:~/session</span>
         </div>
         <button onClick={clearChat} className="text-[#666] hover:text-white transition-colors" title="Clear History">
             <FaEraser />
         </button>
      </div>

      {/* MESSAGES */}
      <div 
        ref={scrollContainerRef}
        onScroll={handleScroll}
        className="flex-1 overflow-y-auto p-6 md:p-10 space-y-8 scroll-smooth"
      >
        <AnimatePresence>
          {messages.map((msg, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}
            >
              {/* Avatar */}
              <div className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 border 
                  ${msg.role === 'user' ? 'bg-[#00f2ff]/10 border-[#00f2ff]/30 text-[#00f2ff]' : 'bg-[#fff]/5 border-[#fff]/10 text-[#fff]'}`}>
                  {msg.role === 'user' ? <FaUser size={14} /> : <FaRobot size={16} />}
              </div>

              {/* Bubble */}
              <div className={`flex flex-col max-w-[80%]`}>
                  <span className={`text-xs mb-1 font-mono opacity-50 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
                      {msg.role === 'user' ? 'YOU' : 'AI CORE'}
                  </span>
                  <div className={`p-4 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap shadow-lg backdrop-blur-md
                      ${msg.role === 'user' 
                        ? 'bg-gradient-to-br from-[#00f2ff]/20 to-[#00a8ff]/20 border border-[#00f2ff]/30 text-white rounded-tr-none' 
                        : 'bg-[#1a1a24] border border-white/5 text-[#d0d0d0] rounded-tl-none font-mono'}`}>
                     {msg.content}
                  </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        <div ref={messagesEndRef} />
      </div>

      {/* INPUT */}
      <div className="p-6 bg-gradient-to-t from-[#050510] to-transparent">
        <div className="relative group transition-all">
          <div className="absolute inset-0 bg-gradient-to-r from-[#00f2ff] to-[#ff00ff] rounded-full blur opacity-20 group-hover:opacity-40 transition-opacity duration-500" />
          <div className="relative flex items-center bg-[#0a0a12] border border-white/10 rounded-full px-6 py-4 shadow-xl">
             <FaTerminal className="text-[#666] mr-4" />
             <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ex: Create a React component for a login form..."
                className="flex-1 bg-transparent border-none outline-none text-white placeholder-[#555] font-light"
                disabled={isLoading}
             />
             <button 
                onClick={sendMessage}
                disabled={isLoading || !input.trim()}
                className={`ml-4 p-2 rounded-full transition-all duration-300
                    ${input.trim() ? 'bg-[#00f2ff] text-black rotate-0 opacity-100 hover:scale-110' : 'bg-[#333] text-[#555] -rotate-45 opacity-50 cursor-not-allowed'}`}
             >
                <FaPaperPlane size={14} />
             </button>
          </div>
        </div>
        <div className="text-center mt-3">
             <span className="text-[10px] text-[#444] uppercase tracking-widest">Powering Innovation</span>
        </div>
      </div>
    </div>
  );
}
