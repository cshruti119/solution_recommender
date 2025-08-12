import { PRODUCTS } from "../data/productData";

// Generate a random order ID
const generateRandomOrderId = () => {
  const prefix = 'ORD';
  const randomDigits = Math.floor(10000 + Math.random() * 90000);
  return `${prefix}${randomDigits}`;
};

// Generate a random date within the last 120 days
const generateRandomDate = () => {
  const now = new Date();
  const daysAgo = Math.floor(Math.random() * 120);
  const randomDate = new Date(now);
  randomDate.setDate(now.getDate() - daysAgo);
  return randomDate.toISOString().split('T')[0];
};

// Select random products from the PRODUCTS array
const selectRandomProducts = () => {
  const numProducts = Math.floor(Math.random() * 3) + 1;
  const selectedProducts = [];
  const availableProducts = [...PRODUCTS];

  for (let i = 0; i < numProducts; i++) {
    if (availableProducts.length === 0) break;

    const randomIndex = Math.floor(Math.random() * availableProducts.length);
    const product = availableProducts.splice(randomIndex, 1)[0];
    const quantity = Math.floor(Math.random() * 3) + 1; // 1 to 3 items

    selectedProducts.push({
      productId: product.productId,
      productName: product.productName,
      quantity: quantity,
      partnerId: product.partnerId,
      price: product.price
    });
  }

  return selectedProducts;
};

// Generate random orders
const generateRandomOrders = (count = 5) => {
  return Array.from({ length: count }, () => ({
    orderId: generateRandomOrderId(),
    purchaseDate: generateRandomDate(),
    products: selectRandomProducts()
  })).sort((a, b) => new Date(b.purchaseDate) - new Date(a.purchaseDate));
};

export const getRecentOrdersForUser = () => {
  const orders = generateRandomOrders();
  orders.sort(
    (a, b) => new Date(b.purchaseDate) - new Date(a.purchaseDate),
  );
  return orders.slice(0, 5);
};
