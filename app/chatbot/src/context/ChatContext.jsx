import React, { createContext, useContext, useState } from "react";

const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [selectedProblemReasonType, setSelectedProblemReasonType] =
    useState(null);
  const [selectedProblemSubReason, setSelectedProblemSubReason] =
    useState(null);
  const [userInput, setUserInput] = useState("");
  const [userFeedback, setUserFeedback] = useState("");
  const [allMessages, setAllMessages] = useState([]);

  return (
    <ChatContext.Provider
      value={{
        selectedOrder,
        setSelectedOrder,
        selectedProduct,
        setSelectedProduct,
        selectedProblemReasonType,
        setSelectedProblemReasonType,
        selectedProblemSubReason,
        setSelectedProblemSubReason,
        userInput,
        setUserInput,
        userFeedback,
        setUserFeedback,
        allMessages,
        setAllMessages,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};

export const useChatContext = () => useContext(ChatContext);
