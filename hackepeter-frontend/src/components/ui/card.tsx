import * as React from "react";
import { useState } from "react";

import { cn } from "@/lib/utils";

const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("rounded-lg border bg-card text-card-foreground shadow-sm", className)} {...props} />
));
Card.displayName = "Card";

const CardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("flex flex-col space-y-1.5 p-6", className)} {...props} />
  )
);
CardHeader.displayName = "CardHeader";

const CardTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h3 ref={ref} className={cn("text-2xl font-semibold leading-none tracking-tight", className)} {...props} />
  )
);
CardTitle.displayName = "CardTitle";

const CardDescription = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => (
    <p ref={ref} className={cn("text-sm text-muted-foreground", className)} {...props} />
  )
);
CardDescription.displayName = "CardDescription";

const CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
);
CardContent.displayName = "CardContent";

const CardFooter = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => <div ref={ref} className={cn("flex items-center p-6 pt-0", className)} {...props} />
);
CardFooter.displayName = "CardFooter";

function ChatWindow({ selectedContent }) {
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState(""); // Current message input

  const sendMessage = async () => {
    if (message) {
      // Directly set name to "user" for the outgoing message
      const userMessage = { user: message.trim() };
      setMessages((messages) => [...messages, userMessage]);
      console.log(Object.values(selectedContent.metadata.sources));
      console.log(messages);
      // Reset message input
      setMessage("");

      fetch("http://127.0.0.1:8000/converse/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          science: selectedContent.metadata.science,
          sources: Object.values(selectedContent.metadata.sources),
          history: messages,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          const model_message = data;

          // const aiResponse = `AI:: ${model_message}`;
          const aiResponse = { model: model_message };
          setMessages((messages) => [...messages, aiResponse]);
        })
        .catch((error) => console.error("Error:", error));
    }
  };

  return (
    <div className="chat-window" style={{ border: "1px solid #ccc", padding: "10px", marginTop: "20px" }}>
      <div
        className="messages"
        style={{
          height: "200px",
          overflowY: "scroll",
          marginBottom: "10px",
          border: "1px solid #ccc",
          padding: "10px",
          backgroundColor: "#f0f0f0",
        }}
      >
        <div className="messages-display">
          {messages.map((msg, index) => (
            <div key={index}>
              {/* Check if the message is from the user or the model and display accordingly */}
              {msg.user ? `User: ${msg.user}` : `Model: ${msg.model}`}
            </div>
          ))}
        </div>
        {/* {messages.map((msg, index) => (
          <div key={index} style={{ marginBottom: "5px" }}>
            {msg}
          </div>
        ))} */}
      </div>
      <textarea
        placeholder="Ask a follow up question ..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        style={{
          width: "100%",
          padding: "10px",
          boxSizing: "border-box",
          border: "1px solid #ccc",
          height: "50px",
          resize: "none",
        }}
      />
      <button
        onClick={sendMessage}
        style={{ width: "100%", padding: "10px", boxSizing: "border-box", border: "1px solid #ccc", marginTop: "10px" }}
      >
        Send
      </button>
    </div>
  );
}

export default ChatWindow;

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent, ChatWindow };
