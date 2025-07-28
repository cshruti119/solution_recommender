import React, { useEffect } from "react";
import { FooterInput } from "./FooterInput";
import { TypingIndicator } from "./TypingIndicator";
import { MessageBubble } from "./MessageBubble";
import { useChatbotFlow } from "../context/useChatbotFlow";
import {
  BG_COLOR,
  INITIAL_GREETING_MESSAGE,
  ISSUE_TYPES,
  PRIMARY_COLOR,
  SELECT_ISSUE_MESSAGE,
  SENDER,
  TITLE_COLOR,
} from "../data/constants";

export const ChatbotUI = () => {
  const {
    messages,
    step,
    input,
    loading,
    setInput,
    messagesEndRef,
    handleIssueTypeSelection,
    handleOrderSelection,
    handleProductSelection,
    handleReasonSelection,
    handleSubReasonSelection,
    handleSolutionChoice,
    handleFeedback,
    handleSendDescription,
    handleOtherReasonSubmit,
    handleFeedbackSubmit,
    hasGreeted,
    showMessage,
  } = useChatbotFlow();

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if (
      !hasGreeted.current &&
      messages.length === 0 &&
      step === "initial_greeting"
    ) {
      hasGreeted.current = true;
      showMessage(SENDER.BOT, INITIAL_GREETING_MESSAGE);
      showMessage(SENDER.BOT, SELECT_ISSUE_MESSAGE, "issue_types", ISSUE_TYPES);
    }
  }, [messages, step]);

  return (
    <div
      className="min-h-screen flex items-center justify-center p-4"
      style={{ backgroundColor: BG_COLOR }}
    >
      <div className="w-full max-w-[50%] bg-white rounded-2xl shadow-lg flex flex-col h-[90vh]">
        <header className="flex flex-col items-start justify-between px-6 py-4 border-b">
          <h1 className="text-2xl font-bold" style={{ color: TITLE_COLOR }}>
            Service & Help Chatbot
          </h1>
          <div className="flex items-center space-x-2">
            <span className="h-3 w-3 rounded-full bg-green-500 animate-ping" />
            <span
              className="text-sm font-medium"
              style={{ color: PRIMARY_COLOR }}
            >
              Online
            </span>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}
            >
              <MessageBubble
                key={i}
                message={msg}
                onTypeSelect={handleIssueTypeSelection}
                onOrderSelect={handleOrderSelection}
                onProductSelect={handleProductSelection}
                onReasonSelect={handleReasonSelection}
                onSubReasonSelect={handleSubReasonSelection}
                onSolutionSelect={handleSolutionChoice}
                onReEngage={handleFeedback}
              />
            </div>
          ))}
          {loading && <TypingIndicator />}
          <div ref={messagesEndRef} />
        </div>

        <FooterInput
          step={step}
          input={input}
          setInput={setInput}
          onSendDescription={handleSendDescription}
          onOtherReasonSubmit={handleOtherReasonSubmit}
          onFeedbackSubmit={handleFeedbackSubmit}
        />
      </div>
    </div>
  );
};
