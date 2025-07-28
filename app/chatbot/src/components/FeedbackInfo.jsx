import React, { useState } from "react";
import { PRIMARY_COLOR } from "../data/constants";
import { MessageCircle } from "lucide-react";

export const FeedbackInfo = ({ message, feedbackPlaceholder, onSubmit }) => {
  const [feedback, setFeedback] = useState("");

  return (
    <div className="flex items-start space-x-2 mb-2">
      <div
        className="p-2 rounded-full flex-shrink-0"
        style={{
          backgroundColor: PRIMARY_COLOR,
        }}
      >
        <MessageCircle size={24} color="white" />
      </div>
      <div className="bg-white p-4 rounded-lg shadow w-4/5 border">
        <p className="mb-2">{message}</p>
        <textarea
          className="w-full p-2 border rounded mb-2"
          rows={3}
          placeholder={feedbackPlaceholder}
          value={feedback}
          onChange={(e) => setFeedback(e.target.value)}
        />
        <button
          className={`bg-red-600 text-white px-4 py-2 rounded ${!feedback ? " opacity-50" : ""}`}
          disabled={!feedback}
          onClick={() => onSubmit(feedback)}
        >
          Submit Feedback
        </button>
      </div>
    </div>
  );
};
