import React from "react";
import { MessageCircle } from "lucide-react";
import { GREY_COLOR, PRIMARY_COLOR } from "../data/constants";

export const OrdersList = ({
  message,
  ordersList,
  onOrderSelect,
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
        {ordersList.map((o, idx) => (
          <div
            key={idx}
            onClick={() => onOrderSelect(o)}
            className="p-3 mb-2 border rounded cursor-pointer"
          >
            <strong>Order {o.orderId}</strong>
            <div className="text-sm text-gray-500">
              Purchased on {o.purchaseDate}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
