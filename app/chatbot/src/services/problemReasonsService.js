import { BUSINESS_INCIDENT_REASON_TYPES } from "../data/constants";

export const fetchMatchingProblemReasons = async (searchTerm) => {
  // Optionally, you can filter BUSINESS_INCIDENT_REASON_TYPES based on searchTerm if needed
  await new Promise((r) => setTimeout(r, 1000));
  return BUSINESS_INCIDENT_REASON_TYPES;
};
