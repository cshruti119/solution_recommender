export const PRIMARY_COLOR = "#dc001d";
export const TITLE_COLOR = "#777777";
export const GREY_COLOR = "#E5E5E5";
export const TEXT_COLOR = "#212121";
export const BG_COLOR = "rgb(240,240,240)";

export const BUSINESS_INCIDENT_REASON_TYPES = [
  {
    reasonType: "Product not working",
    businessIncidentReasons: [
      { reason: "Material not liked" },
      { reason: "Color / pattern not liked" },
      { reason: "Color / pattern does not match combination item" },
      { reason: "Expected something better for the price" },
      { reason: "Shape / cut not liked" },
    ],
  },
  {
    reasonType: "Catalog illustration",
    businessIncidentReasons: [
      { reason: "Item different than described / illustrated" },
      { reason: "Color / pattern different than described / illustrated" },
    ],
  },
  {
    reasonType: "Delivery / Order",
    businessIncidentReasons: [
      { reason: "Delivered too late / delivery date not met" },
      { reason: "Delivered incorrectly / ordered incorrectly" },
      { reason: "Delivered twice / ordered twice" },
      { reason: "Delivery incomplete" },
      { reason: "Ordered several items / colors for selection" },
      { reason: "Ordered several sizes for selection" },
    ],
  },
  {
    reasonType: "Quality",
    businessIncidentReasons: [
      { reason: "Item damaged / broken" },
      { reason: "Material / processing defect" },
      { reason: "Does not work" },
      { reason: "Transport damage" },
      { reason: "Other quality problems" },
    ],
  },
  {
    reasonType: "Other reasons",
    businessIncidentReasons: [
      { reason: "KC / KD cancellation" },
      { reason: "No longer needed" },
      { reason: "Cancelled earlier" },
      { reason: "Payment difficulties" },
      { reason: "Suspected fraud" },
      { reason: "Other delivery / order-related reasons" },
      { reason: "Other" },
    ],
  },
];

export const ISSUE_TYPES = ["Product", "Order", "Payment", "Warranty", "Other"];

export const SENDER = {
  USER: "user",
  BOT: "bot",
};

export const SOLUTIONS = [
  "Price Discount",
  "Compensation Code",
  "Spare Parts Order",
  "Repair Request",
  "Return",
];

// Messages
export const INITIAL_GREETING_MESSAGE = "Hi! How can I help you today?";
export const THANK_YOU_MESSAGE = "Thank you for feedback!";
export const SELECT_ISSUE_MESSAGE =
  "Please select the type of issue you are experiencing:";
export const CALL_CUSTOMER_SUPPORT_MESSAGE =
  "For other issues, please call 1-800-123-4567.";
export const CURRENTLY_UNSUPPORTED_MESSAGE =
  "Currently, we only support product-related issues in this chat. For other concerns, please contact our support team at 1-800-123-4567.";
export const SELECT_FROM_RECENT_ORDERS_MESSAGE =
  "Please select the order you need help with from your recent purchases:";
export const NO_RECENT_ORDERS_FOUND_MESSAGE =
  "No recent orders found. Please describe your issue:";
export const SELECT_PROBLEM_SUBREASON_MESSAGE =
  "Please select the specific issue you are facing with this product:";
export const SOLUTION_NOT_RESOLVED_FEEDBACK_MESSAGE = `We're sorry the solution did not resolve your issue. Please let us know why in the box below, so we can improve. If you'd like to connect with a support agent, please call 1-800-123-4567`;
export const FEEDBACK_THANK_YOU_MESSAGE =
  "Thank you for confirming. We will now proceed with your request and initiate the next steps. You will receive a confirmation and further instructions shortly. If you have any feedback about this process, please let us know!";
