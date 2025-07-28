import React from "react";
import { GREY_COLOR, PRIMARY_COLOR } from "../data/constants";
import { MessageCircle } from "lucide-react";

export const SelectionCard = ({
  message,
  options,
  onOptionSelect,
  showChatIcon = true,
}) => {
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
      <div
        className="bg-white p-4 rounded-lg w-4/5"
        style={{ border: `2px solid ${GREY_COLOR}` }}
      >
        <p className="mb-2">{message}</p>
        {options.map((option, idx) => {
          let label = option;
          if (typeof option === "object") {
            label =
              option.productName ||
              option.orderId ||
              option.reason ||
              option.reasonType ||
              JSON.stringify(option);
          }
          return (
            <button
              key={idx}
              onClick={() => onOptionSelect(option)}
              className="block w-full text-left p-3 mb-2 border rounded cursor-pointer"
              style={{
                backgroundColor: GREY_COLOR,
                color: "#212121",
              }}
            >
              {label}
            </button>
          );
        })}
      </div>
    </div>
  );
};
