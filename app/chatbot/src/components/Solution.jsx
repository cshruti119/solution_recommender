import React from "react";
import { PRIMARY_COLOR } from "../data/constants";
import { MessageCircle } from "lucide-react";

export const Solution = ({ solution, showChatIcon = true }) => {
  return (
    <div className="flex items-start space-x-2 mb-2 w-4/5">
      <div
        className="p-2 rounded-full flex-shrink-0"
        style={{
          backgroundColor: showChatIcon ? PRIMARY_COLOR : "transparent",
        }}
      >
        <MessageCircle size={24} color="white" />
      </div>
      <div className="bg-white p-4 rounded-lg shadow w-4/5">
        <p>Based on your problem, here is a recommended solution:</p>
        <div className="flex items-center gap-3 text-grey-800 p-4 rounded-xl border border-grey-200 shadow-md font-semibold text-base md:text-lg">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="currentColor"
            className="w-6 h-6 flex-shrink-0"
          >
            <path d="M12 1.5a.75.75 0 0 1 .75.75V4.5a.75.75 0 0 1-1.5 0V2.25A.75.75 0 0 1 12 1.5ZM12 19.5a.75.75 0 0 1 .75.75V22.5a.75.75 0 0 1-1.5 0V20.25a.75.75 0 0 1 .75-.75ZM20.25 12a.75.75 0 0 1-.75.75H18a.75.75 0 0 1 0-1.5h1.5a.75.75 0 0 1 .75.75ZM3.75 12a.75.75 0 0 1-.75.75H2.25a.75.75 0 0 1 0-1.5H3a.75.75 0 0 1 .75.75ZM12 6a6 6 0 1 0 0 12 6 6 0 0 0 0-12ZM9.75 8.25a.75.75 0 0 0-1.5 0v1.5a.75.75 0 0 0 1.5 0v-1.5ZM14.25 8.25a.75.75 0 0 0-1.5 0v1.5a.75.75 0 0 0 1.5 0v-1.5ZM9.75 14.25a.75.75 0 0 0-1.5 0v1.5a.75.75 0 0 0 1.5 0v-1.5ZM14.25 14.25a.75.75 0 0 0-1.5 0v1.5a.75.75 0 0 0 1.5 0v-1.5Z" />
          </svg>
          <span>{solution}</span>
        </div>
      </div>
    </div>
  );
};
