import React from "react";
import { Message } from "./Message";
import { SelectionCard } from "./SelectionCard";
import { SENDER } from "../data/constants";
import { OrdersList } from "./OrdersList";
import { Solution } from "./Solution";
import { FeedbackInfo } from "./FeedbackInfo";

export const MessageBubble = ({ message, ...handlers }) => {
  const {
    onTypeSelect,
    onOrderSelect,
    onProductSelect,
    onReasonSelect,
    onSolutionSelect,
    onReEngage,
    onSubReasonSelect,
  } = handlers;
  const isUser = message.sender === SENDER.USER;

  if (message.type === "text") {
    return <Message message={message.text} isUser={isUser} />;
  }

  if (message.type === "issue_types") {
    return (
      <SelectionCard
        message={message.text}
        options={message.data}
        onOptionSelect={onTypeSelect}
        showChatIcon={false}
      />
    );
  }

  if (message.type === "order_list") {
    return (
      <OrdersList
        message={message.text}
        ordersList={message.data}
        onOrderSelect={onOrderSelect}
      />
    );
  }

  if (message.type === "products_in_order") {
    return (
      <SelectionCard
        message={message.text}
        options={message.data}
        onOptionSelect={onProductSelect}
      />
    );
  }

  if (message.type === "problem_reasons") {
    return (
      <SelectionCard
        message={message.text}
        options={message.data}
        onOptionSelect={onReasonSelect}
      />
    );
  }

  if (message.type === "problem_subreasons") {
    return (
      <SelectionCard
        message={message.text}
        options={message.data}
        onOptionSelect={onSubReasonSelect}
      />
    );
  }

  if (message.type === "solution_presented") {
    return <Solution solution={message.data} />;
  }

  if (message.type === "solution_options") {
    return (
      <SelectionCard
        message={message.text}
        options={message.data}
        onOptionSelect={onSolutionSelect}
      />
    );
  }

  if (message.type === "feedback") {
    return (
      <FeedbackInfo
        message={message.text}
        feedbackPlaceholder={"Please provide input here..."}
        onSubmit={onReEngage}
      />
    );
  }

  return null;
};
