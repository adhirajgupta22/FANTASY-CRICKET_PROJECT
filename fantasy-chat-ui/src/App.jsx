// App.jsx
import {Routes, Route, useNavigate } from "react-router-dom";
import { useState } from "react";
import axios from "axios";
import "./App.css"; // Ensure you have Tailwind CSS set up in your project
import HomePage from "./pages/HomePage";
import ChatPage from "./pages/chatPage";

// --- Dashboard Page ---
// function Dashboard() {
//   const navigate = useNavigate();
//   return (
//     <div className="flex flex-col h-screen bg-gradient-to-br from-zinc-900 to-black text-white items-center justify-center">
//       <div className="bg-zinc-800 rounded-3xl shadow-2xl p-12 flex flex-col items-center">
//         <h1 className="text-4xl font-bold mb-4 text-blue-400">Welcome to ChatApp</h1>
//         <p className="text-zinc-400 mb-8 text-lg">Your AI-powered assistant is here!</p>
//         <button
//           onClick={() => navigate("/chat")}
//           className="bg-blue-600 hover:bg-blue-500 px-6 py-3 rounded-xl text-white font-semibold shadow-lg transition-all"
//         >
//           Go to Chat Page
//         </button>
//       </div>
//     </div>
//   );
// }

// --- Chat Page ---
// function ChatPage() {
//   const [input, setInput] = useState("");
//   const [messages, setMessages] = useState([]);
//   const [chats, setChats] = useState([{ id: 1, name: "Chat 1" }]);
//   const [currentChat, setCurrentChat] = useState(1);

//   const sendMessage = async () => {
//     if (!input.trim()) return;
//     const userMessage = { role: "user", content: input };
//     setMessages((prev) => [...prev, userMessage]);
//     setInput("");
//     try {
//       const response = await axios.post("http://localhost:5000/chat", {
//         message: input,
//       });
//       if (response.data.messages) {
//         const agentMessages = response.data.messages.map((msg) => ({
//           role: "agent",
//           content: msg,
//         }));
//         setMessages((prev) => [...prev, ...agentMessages]);
//       } else {
//         setMessages((prev) => [
//           ...prev,
//           { role: "agent", content: "Something went wrong." },
//         ]);
//       }
//     } catch (error) {
//       setMessages((prev) => [
//         ...prev,
//         { role: "agent", content: "Server error: " + error.message },
//       ]);
//     }
//   };

//   const handleNewChat = () => {
//     const newId = chats.length + 1;
//     setChats([...chats, { id: newId, name: `Chat ${newId}` }]);
//     setCurrentChat(newId);
//     setMessages([]);
//   };

//   return (
//     <div className="flex h-screen bg-gradient-to-br from-zinc-900 to-black text-white">
//       {/* Sidebar / Navbar */}
//       <div className="w-72 bg-zinc-800 flex flex-col border-r border-zinc-700">
//         <div className="flex items-center justify-between px-4 py-5 border-b border-zinc-700">
//           <span className="text-xl font-semibold text-blue-400">Chats</span>
//           <button
//             className="bg-blue-600 hover:bg-blue-500 text-white px-3 py-1 rounded-lg text-sm font-medium"
//             onClick={handleNewChat}
//           >
//             + New Chat
//           </button>
//         </div>
//         <div className="flex-1 overflow-y-auto p-4 space-y-2">
//           {chats.map((chat) => (
//             <div
//               key={chat.id}
//               onClick={() => {
//                 setCurrentChat(chat.id);
//                 setMessages([]);
//               }}
//               className={`cursor-pointer px-4 py-2 rounded-lg transition-all ${
//                 chat.id === currentChat
//                   ? "bg-zinc-700 text-white font-bold"
//                   : "text-zinc-400 hover:bg-zinc-700"
//               }`}
//             >
//               {chat.name}
//             </div>
//           ))}
//         </div>
//       </div>
//       {/* Main Chat Area */}
//       <div className="flex-1 flex flex-col">
//         <div className="flex-1 overflow-y-auto p-8 space-y-4 bg-zinc-900">
//           {messages.length === 0 ? (
//             <div className="h-full flex items-center justify-center text-zinc-500 text-xl">
//               Start a new conversation
//             </div>
//           ) : (
//             messages.map((msg, idx) => (
//               <div
//                 key={idx}
//                 className={`max-w-2xl p-4 rounded-xl shadow-lg ${
//                   msg.role === "user"
//                     ? "bg-blue-700 self-end"
//                     : "bg-zinc-800 self-start"
//                 }`}
//               >
//                 <span className="block text-xs mb-1 text-zinc-400">
//                   {msg.role === "user" ? "You" : "Agent"}
//                 </span>
//                 <span className="text-base">{msg.content}</span>
//               </div>
//             ))
//           )}
//         </div>
//         {/* Input Box */}
//         <div className="w-full border-t border-zinc-700 p-5 bg-zinc-900">
//           <div className="max-w-3xl mx-auto flex gap-3">
//             <textarea
//               rows="1"
//               className="flex-1 bg-zinc-800 rounded-xl p-3 text-white resize-none focus:outline-none"
//               placeholder="Type your message..."
//               value={input}
//               onChange={(e) => setInput(e.target.value)}
//               onKeyDown={(e) =>
//                 e.key === "Enter" &&
//                 !e.shiftKey &&
//                 (e.preventDefault(), sendMessage())
//               }
//             />
//             <button
//               onClick={sendMessage}
//               className="bg-blue-600 hover:bg-blue-500 px-6 py-2 rounded-xl text-white font-semibold"
//             >
//               Send
//             </button>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

// --- Main App with Routing ---
function App() {
  return (
    <div className="min-h-screen">
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/chat" element={<ChatPage/>} />
      </Routes>
    </div>
  );
}

export default App;
