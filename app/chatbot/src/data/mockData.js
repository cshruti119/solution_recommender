export const mockPurchasedOrders = [
  {
    orderId: "ORD12345",
    purchaseDate: "2025-06-15",
    products: [
      {
        productId: "PROD001",
        productName: "Wireless Headphones",
        quantity: 1,
        price: 99.99,
      },
      {
        productId: "PROD002",
        productName: "Charging Cable",
        quantity: 2,
        price: 9.99,
      },
    ],
  },
  {
    orderId: "ORD67890",
    purchaseDate: "2025-05-20",
    products: [
      {
        productId: "PROD003",
        productName: "Smartwatch X",
        quantity: 1,
        price: 199.99,
      },
    ],
  },
  {
    orderId: "ORD44556",
    purchaseDate: "2025-04-10",
    products: [
      {
        productId: "PROD004",
        productName: "USB-C Hub",
        quantity: 1,
        price: 49.99,
      },
      {
        productId: "PROD005",
        productName: "External SSD 500GB",
        quantity: 1,
        price: 79.99,
      },
    ],
  },
  {
    orderId: "ORD99887",
    purchaseDate: "2025-07-05",
    products: [
      {
        productId: "PROD006",
        productName: "Gaming Keyboard",
        quantity: 1,
        price: 120.0,
      },
      {
        productId: "PROD007",
        productName: "Gaming Mouse",
        quantity: 1,
        price: 60.0,
      },
    ],
  },
  {
    orderId: "ORD00112",
    purchaseDate: "2025-06-01",
    products: [
      {
        productId: "PROD008",
        productName: "Monitor Stand",
        quantity: 1,
        price: 35.0,
      },
    ],
  },
];

export const mockProblemReasonsForElectricalProduct = [
  "No sound",
  "Mic broken",
  "Conn. issue",
  "Battery drains",
];

export const mockProblemReasonsForChargingIssues = [
  "Not charging",
  "Damaged",
  "Slow charging",
];

export const mockProblemReasonsForQualityIssues = [
  "Product not working",
  "Missing parts",
  "Damaged",
];
