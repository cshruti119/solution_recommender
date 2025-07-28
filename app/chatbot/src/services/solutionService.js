import { SOLUTIONS } from "../data/constants";

export const fetchMatchingSolution = async (reason) => {
  await new Promise((r) => setTimeout(r, 500));
  // Simple logic: pick a solution based on reason, or default to "Return"
  let sol;
  if (/price|cost/i.test(reason)) sol = SOLUTIONS[0];
  else if (/damage|broken|compensate/i.test(reason)) sol = SOLUTIONS[1];
  else if (/part|missing/i.test(reason)) sol = SOLUTIONS[2];
  else if (/repair|fix/i.test(reason)) sol = SOLUTIONS[3];
  else sol = SOLUTIONS[4];
  return sol;
};
