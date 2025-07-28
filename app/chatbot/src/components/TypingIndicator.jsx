import React from "react";
import { PRIMARY_COLOR } from "../data/constants";
import { MessageCircle } from "lucide-react";

export const TypingIndicator = () => {
  return (
    <div className="flex items-center space-x-2 self-start">
      <div
        className="p-2 rounded-full flex-shrink-0"
        style={{ backgroundColor: PRIMARY_COLOR }}
      >
        <MessageCircle size={24} color="white" />
      </div>

      <div className="self-start p-4 bg-gray-100 rounded-lg animate-pulse w-max">
        Thinking…
      </div>
    </div>
  );
};
