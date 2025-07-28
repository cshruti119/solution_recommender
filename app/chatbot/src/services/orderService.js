import { mockPurchasedOrders } from "../data/mockData";

export const getRecentOrdersForUser = () => {
  const orders = mockPurchasedOrders;
  mockPurchasedOrders.sort(
    (a, b) => new Date(b.purchaseDate) - new Date(a.purchaseDate),
  );
  return orders.slice(0, 5);
};
