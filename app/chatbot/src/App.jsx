import React from "react";
import { ChatProvider } from "./context/ChatContext";
import { ChatbotUI } from "./components/ChatbotUI";

export default function App() {
  return (
    <ChatProvider>
      <ChatbotUI />
    </ChatProvider>
  );
}
