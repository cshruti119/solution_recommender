import React from "react";
import { UserInput } from "./UserInput";
import { useChatContext } from "../context/ChatContext";
import { THANK_YOU_MESSAGE } from "../data/constants";

export const FooterInput = ({
  step,
  input,
  setInput,
  onSendDescription,
  onOtherReasonSubmit,
}) => {
  const { allMessages } = useChatContext();

  if (step === "describe_issue") {
    return (
      <UserInput
        input={input}
        setInput={setInput}
        onFeedbackSubmit={onSendDescription}
        placeholder={"Describe your issue…"}
      />
    );
  }

  if (step === "other_reason_input") {
    return (
      <UserInput
        input={input}
        setInput={setInput}
        onFeedbackSubmit={onOtherReasonSubmit}
        placeholder={"Enter reason…"}
      />
    );
  }

  if (
    step === "feedback" ||
    (allMessages &&
      allMessages.length > 0 &&
      allMessages[allMessages.length - 1].text === THANK_YOU_MESSAGE)
  ) {
    return null;
  }

  return (
    <div className="border-t p-4 text-center text-gray-500 italic">
      Please select an option above.
    </div>
  );
};
