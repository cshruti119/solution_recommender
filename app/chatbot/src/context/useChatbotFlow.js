import { useRef, useState } from "react";
import { getRecentOrdersForUser } from "../services/orderService";
import { fetchMatchingProblemReasons } from "../services/problemReasonsService";
import { useSolutionApi } from "../hooks/useSolutionApi";
import {
  CALL_CUSTOMER_SUPPORT_MESSAGE,
  CURRENTLY_UNSUPPORTED_MESSAGE,
  FEEDBACK_THANK_YOU_MESSAGE,
  NO_RECENT_ORDERS_FOUND_MESSAGE,
  SELECT_FROM_RECENT_ORDERS_MESSAGE,
  SELECT_PROBLEM_SUBREASON_MESSAGE,
  SENDER,
  SOLUTION_NOT_RESOLVED_FEEDBACK_MESSAGE,
  THANK_YOU_MESSAGE,
} from "../data/constants";
import { useChatContext } from "./ChatContext";
import { fetchMatchingSolution } from "../services/solutionService";

export const useChatbotFlow = () => {
  const [messages, setMessages] = useState([]);
  const [step, setStep] = useState("initial_greeting");
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const hasGreeted = useRef(false);

  const {
    setSelectedOrder,
    setSelectedProduct,
    selectedProblemReason,
    setSelectedProblemReason,
    selectedProduct,
    setSelectedProblemSubReason,
    setUserInput,
    setUserFeedback,
    setAllMessages,
  } = useChatContext();

  const { getSolution, data: solutionData, isError } = useSolutionApi();

  const showMessage = (sender, text, type = "text", data = null) => {
    setMessages((msgs) => {
      const newMsgs = [
        ...msgs,
        { sender, text, type, data, timestamp: new Date() },
      ];
      setAllMessages && setAllMessages(newMsgs);
      return newMsgs;
    });
  };

  const sendContactSupportMessage = () => {
    showMessage(SENDER.BOT, CALL_CUSTOMER_SUPPORT_MESSAGE);
    setStep("contact_support");
  };

  const handleIssueTypeSelection = (type) => {
    showMessage(SENDER.USER, type);
    if (type === "Other") {
      sendContactSupportMessage();
      return;
    }
    if (type !== "Product") {
      showMessage(SENDER.BOT, CURRENTLY_UNSUPPORTED_MESSAGE);
      setStep("conversation_ended");
      return;
    }
    const recent = getRecentOrdersForUser();
    if (recent.length) {
      showMessage(
        SENDER.BOT,
        SELECT_FROM_RECENT_ORDERS_MESSAGE,
        "order_list",
        recent,
      );
      setStep("select_order");
    } else {
      showMessage(SENDER.BOT, NO_RECENT_ORDERS_FOUND_MESSAGE);
      setStep("describe_issue");
    }
  };

  const handleOrderSelection = (order) => {
    setSelectedOrder(order);
    showMessage(SENDER.USER, `Order ${order.orderId}`);
    showMessage(
      SENDER.BOT,
      `Which product in ${order.orderId}?`,
      "products_in_order",
      order.products,
    );
    setStep("select_product");
  };

  const fetchProblemReasons = async (productName) => {
    setLoading(true);
    let reasons = [];
    try {
      reasons = await fetchMatchingProblemReasons(productName);
    } catch (error) {
      console.error("Error fetching problem reasons:", error);
    }
    setLoading(false);
    return reasons;
  };

  const handleProductSelection = async (product) => {
    setSelectedProduct(product);
    showMessage(SENDER.USER, product.productName);
    const reasons = await fetchProblemReasons(product.productName);
    showMessage(
      SENDER.BOT,
      "Select a reason:",
      "problem_reasons",
      reasons.map((r) => r.reasonType),
    );
    setStep("problem_reason_selection");
  };

  const handleReasonSelection = async (reasonType) => {
    setSelectedProblemReason(reasonType);
    showMessage(SENDER.USER, reasonType);
    setSelectedProblemReason(reasonType);
    if (reasonType?.toLowerCase().includes("other")) {
      sendContactSupportMessage();
      return;
    }

    const reasons = await fetchProblemReasons();
    const found = reasons.find((r) => r.reasonType === reasonType);
    if (found && found.businessIncidentReasons.length > 0) {
      showMessage(
        SENDER.BOT,
        SELECT_PROBLEM_SUBREASON_MESSAGE,
        "problem_subreasons",
        found.businessIncidentReasons.map((r) => r.reason),
      );
    }
    setStep("problem_subreason_selection");
  };

  const handleSubReasonSelection = async (subReason) => {
    if (subReason?.toLowerCase().includes("other")) {
      showMessage(SENDER.USER, subReason);
      setSelectedProblemSubReason(subReason);
      sendContactSupportMessage();
      return;
    }

    showMessage(SENDER.USER, subReason);
    setSelectedProblemSubReason(subReason);

    if (selectedProblemReason) {
      console.log(selectedProduct)
      await fetchSolution({
        partnerId: selectedProduct.partnerId,
        product: selectedProduct.productName,
        reason: selectedProblemReason,
        reasonType: subReason
      });
    }
  };

  const handleOtherReasonSubmit = async () => {
    if (!input) return;
    setUserInput(input);
    showMessage(SENDER.USER, `Other: ${input}`);
    setStep("describe_issue");
    setInput("");
  };

  const fetchSolution = async (params) => {
    setLoading(true);
    try {
      const solutionData = await fetchMatchingSolution(params);
      if (solutionData) {
        showMessage(
          SENDER.BOT,
          "Recommended solution:",
          "solution_presented",
          solutionData
        );
      } else {
        showMessage(
          SENDER.BOT,
          "Recommended solution:",
          "solution_presented",
          "No solution found"
        );
      }

      showMessage(
        SENDER.BOT,
        "Are you okay to proceed with this solution?",
        "solution_options",
        ["Yes", "No"]
      );
      setStep("solution_feedback");
    } catch (e) {
      console.error("Error fetching solution:", e);
      showMessage(
        SENDER.BOT,
        "Recommended solution:",
        "solution_presented",
        "Return"
      );
      showMessage(
        SENDER.BOT,
        "Are you okay to proceed with this solution?",
        "solution_options",
        ["Yes", "No"]
      );
      setStep("solution_feedback");
    } finally {
      setLoading(false);
    }
  };

  const handleSolutionChoice = (choice) => {
    showMessage(SENDER.USER, choice);
    if (choice === "Yes") {
      showMessage(SENDER.BOT, FEEDBACK_THANK_YOU_MESSAGE, "feedback");
      setStep("feedback");
    } else {
      showMessage(
        SENDER.BOT,
        SOLUTION_NOT_RESOLVED_FEEDBACK_MESSAGE,
        "feedback",
        [],
      );
      setStep("feedback");
    }
  };

  const handleUserFeedback = (feedback) => {
    setUserFeedback(feedback);
    showMessage(SENDER.USER, `Feedback: ${feedback}`);
    setStep("conversation_ended");
  };

  const handleBotFeedback = () => {
    showMessage(SENDER.BOT, THANK_YOU_MESSAGE);
    setStep("conversation_ended");
  };

  const handleFeedback = (feedback) => {
    handleUserFeedback(feedback);
    handleBotFeedback();
  };

  const handleFeedbackSubmit = () => {
    if (!input) return;
    handleUserFeedback(input);
    handleBotFeedback();
    setInput("");
    setStep("initial_greeting");
  };

  const handleSendDescription = async () => {
    if (!input) return;
    setUserInput(input);
    showMessage(SENDER.USER, input);
    await fetchProblemReasons(input);
    setInput("");
  };

  return {
    messages,
    step,
    input,
    loading,
    setInput,
    messagesEndRef,
    handleIssueTypeSelection,
    handleOrderSelection,
    handleProductSelection,
    handleReasonSelection,
    handleSubReasonSelection,
    handleSolutionChoice,
    handleFeedback,
    handleSendDescription,
    handleOtherReasonSubmit,
    handleFeedbackSubmit,
    hasGreeted,
    showMessage,
    setStep,
  };
};
