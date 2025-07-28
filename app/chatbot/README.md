# Chatbot-UI

A Chatbot for handling after sales customer support in e-commerce flows (product issues, orders, payments, warranties).  

## Getting Started

1. Install dependencies  
   ```bash
   npm install
   ```
2. Start the dev server (runs on port 3000)  
   ```bash
   npm run dev
   ```
3. Open your browser to:  
   ```
   http://localhost:3001
   ```

## Project Structure

```
react-support-chatbot/
├── index.html
├── package.json
├── vite.config.js
├── README.md
└── src/
    ├── components/    # All React UI components
    ├── context/       # React Context and hooks for global state
    ├── data/          # App constants and mock data
    ├── services/      # API/service logic for orders, reasons, solutions
    ├── main.jsx       # React entrypoint
    ├── App.jsx        # App root, wraps ChatbotUI with context
    └── index.css      # Global styles
```

## Available Scripts

- **npm run dev**: Start the local development server on port 3000  
- **npm run build**: Bundle the app for production into `/dist`  
- **npm run preview**: Preview the production build locally
- **npm run format**: Format code using Prettier

## Context & Data Management

This project uses a React Context (`ChatContext`) to store all relevant chatbot state and user selections. The following data is available in the context and can be used for API calls or business logic:

- **selectedOrder**: The order selected by the user
- **selectedProduct**: The product selected by the user
- **selectedProblemReasonType**: The main problem reason type chosen by the user
- **selectedProblemSubReason**: The specific sub reason selected by the user
- **userInput**: Any free-text input provided by the user (e.g., for 'Other' reasons)
- **userFeedback**: Feedback provided by the user after the solution step

All of these values are updated as the user interacts with the chatbot and are accessible anywhere in the app via the `useChatContext` hook.

## Next Steps to check in UI

- Check BI POST API what are all required fields to create BI.
- If `other` is selected, check if the user input is required for issueType, reason as well.
- Check if user accepts the solution, show them id(May be BI number like reclamation, should be unique) so that they could track.
- Show solution details in the end to the user.
- Change the solution UI color.
