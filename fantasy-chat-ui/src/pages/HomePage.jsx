import React from 'react'
import { useNavigate } from 'react-router-dom'

const HomePage = () => {
    const navigate = useNavigate()
  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-zinc-900 to-black text-white items-center justify-center">
      <div className="bg-zinc-800 rounded-3xl shadow-2xl p-12 flex flex-col items-center">
        <h1 className="text-4xl font-bold mb-4 text-blue-400">Welcome to ChatApp</h1>
        <p className="text-zinc-400 mb-8 text-lg">Your AI-powered assistant is here!</p>
        <button
          onClick={() => navigate("/chat")}
          className="bg-blue-600 hover:bg-blue-500 px-6 py-3 rounded-xl text-white font-semibold shadow-lg transition-all cursor-pointer"
        >
          Go to Chat Page
        </button>
      </div>
    </div>
  )
}

export default HomePage;