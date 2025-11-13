"use client";

import { useState, useEffect, useRef } from "react";
import { User, Bot } from "lucide-react";

interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}

export default function HealthcareChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isInitialized, setIsInitialized] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // Initialize bot greeting
  useEffect(() => {
    if (!isInitialized) {
      setMessages([
        {
          role: "assistant",
          content:
            "Hello! I'm your healthcare assistant. How can I help you today?",
          timestamp: new Date().toISOString(),
        },
      ]);
      setIsInitialized(true);
    }
  }, [isInitialized]);

  // Scroll to bottom on new message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      role: "user",
      content: input,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    const currentInput = input;
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch(
        "https://healthcare-chatbot-4-0d6d.onrender.com/chat",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: currentInput }),
        },
      );

      const data = await response.json();

      const assistantMessage: Message = {
        role: "assistant",
        content:
          data.response || data.message || "I'm here to assist you further.",

        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Error:", error);
      const errorMessage: Message = {
        role: "assistant",
        content:
          "I'm sorry, I'm having trouble connecting to the server. Please try again later.",
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100 text-gray-800">
      {/* Header */}
      <div className="p-4 bg-white shadow-md text-center">
        <h1 className="text-2xl font-semibold animate-blue-green-text">
          Healthcare Assistant
        </h1>
        <p className="text-sm text-gray-500">
          Your AI-powered health companion
        </p>
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex gap-3 ${
              message.role === "user" ? "flex-row-reverse" : "flex-row"
            }`}
          >
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                message.role === "user" ? "bg-blue-500" : "bg-gray-300"
              }`}
            >
              {message.role === "user" ? (
                <User className="w-5 h-5 text-white" />
              ) : (
                <Bot className="w-5 h-5 text-gray-700" />
              )}
            </div>

            <div
              className={`max-w-xl px-4 py-3 rounded-2xl ${
                message.role === "user"
                  ? "bg-blue-500 text-white rounded-br-sm"
                  : "bg-white text-gray-800 rounded-bl-sm shadow-sm"
              }`}
            >
              <p className="whitespace-pre-wrap">{message.content}</p>
              <p
                className={`text-xs mt-1 ${
                  message.role === "user" ? "text-blue-100" : "text-gray-500"
                }`}
              >
                {new Date(message.timestamp).toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </p>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-white flex items-center border-t border-gray-200">
        <input
          type="text"
          className="flex-1 p-3 rounded-lg bg-gray-200 text-gray-800 focus:outline-none"
          placeholder="Ask about symptoms, medicine..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyPress}
        />
        <button
          onClick={handleSubmit}
          disabled={isLoading}
          className="ml-3 bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded-lg font-semibold text-white"
        >
          {isLoading ? "..." : "Send"}
        </button>
      </div>

      {/* Disclaimer */}
      <div className="text-center text-yellow-600 text-sm p-2 bg-gray-100 border-t border-gray-200">
        ⚠️ This is for informational purposes only. Always consult healthcare
        professionals for medical advice.
      </div>
    </div>
  );
}
