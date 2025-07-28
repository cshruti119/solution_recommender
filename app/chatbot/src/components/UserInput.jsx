import React from "react";

const primaryColor = "#dc001d";
const textColor = "#212121";

export const UserInput = ({
  input,
  setInput,
  onFeedbackSubmit,
  placeholder,
}) => {
  return (
    <div className="border-t p-4 flex gap-2">
      <input
        className="flex-1 border rounded-full px-4 py-2"
        style={{ color: textColor }}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && onFeedbackSubmit()}
        placeholder={placeholder}
      />
      <button
        onClick={onFeedbackSubmit}
        className={`px-4 py-2 rounded-full ${!input ? " opacity-50" : ""}`}
        style={{ backgroundColor: primaryColor, color: "white" }}
      >
        Submit
      </button>
    </div>
  );
};
