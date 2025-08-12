import { useState, useCallback } from 'react';
import { fetchMatchingSolution } from '../services/solutionService';
import { useChatContext } from '../context/ChatContext';

export function useSolutionApi() {
  const [data, setData] = useState(null);
  const [isError, setIsError] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  const {
    selectedOrder,
    selectedProduct,
    selectedProblemReason,
    selectedProblemSubReason
  } = useChatContext();

  const getSolution = useCallback(async (params) => {
    setIsError(false);
    setIsSuccess(false);
    setData(null);

    try {
      const result = await fetchMatchingSolution(params);
      setData(result);
      setIsSuccess(true);
    } catch (e) {
      setIsError(true);
    }
  }, [selectedOrder, selectedProduct, selectedProblemReason, selectedProblemSubReason]);

  return { data, isError, isSuccess, getSolution };
}

