import React from "react";
import { CircleUser, MessageCircle } from "lucide-react";
import {
  GREY_COLOR,
  PRIMARY_COLOR,
  TEXT_COLOR,
  TITLE_COLOR,
} from "../data/constants";

export const Message = ({ message, isUser }) => {
  if (!isUser) {
    return (
      <div className="flex items-center space-x-2 self-start">
        <div
          className="p-2 rounded-full flex-shrink-0"
          style={{ backgroundColor: PRIMARY_COLOR }}
        >
          <MessageCircle size={24} color="white" />
        </div>

        <div
          className="relative max-w-[90%] bg-white p-4 rounded-lg"
          style={{ color: TEXT_COLOR, border: `2px solid ${GREY_COLOR}` }}
        >
          <p>{message}</p>
        </div>
      </div>
    );
  }

  if (isUser) {
    return (
      <div className="flex flex-row-reverse items-start space-x-2 space-x-reverse self-start w-3/5">
        <div
          className="p-2 rounded-full flex-shrink-0"
          style={{ backgroundColor: TITLE_COLOR }}
        >
          <CircleUser size={24} color="white" />
        </div>
        <div
          className="self-end max-w-[60%] p-3 pr-5 rounded-lg w-full"
          style={{ color: TEXT_COLOR, backgroundColor: GREY_COLOR }}
        >
          {message}
        </div>
      </div>
    );
  }

  return null;
};
