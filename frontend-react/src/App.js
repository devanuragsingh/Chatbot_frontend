import React, { useState, useRef, useEffect } from "react";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);
  const session_id = "user1";

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { text: input, sender: "user" };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMsg.text,
          session_id: session_id,
        }),
      });

      const data = await res.json();

      const botMsg = { text: data.bot, sender: "bot" };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { text: "Error connecting to server ❌", sender: "bot" },
      ]);
    }

    setLoading(false);
  };

  // Auto scroll
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  // Enter key support
  const handleKeyPress = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  return (
    <div style={styles.container}>
      <h2>AI Chatbot 🤖</h2>

      <div style={styles.chatBox}>
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              ...styles.message,
              alignSelf: msg.sender === "user" ? "flex-end" : "flex-start",
              background: msg.sender === "user" ? "#3b82f6" : "#10b981",
            }}
          >
            {msg.text}
          </div>
        ))}

        {loading && (
          <div style={{ ...styles.message, alignSelf: "flex-start" }}>
            Bot is typing...
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      <div style={styles.inputArea}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyPress}
          style={styles.input}
          placeholder="Type a message..."
        />
        <button onClick={sendMessage} style={styles.button}>
          Send
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    textAlign: "center",
    marginTop: "20px",
    fontFamily: "Arial",
  },
  chatBox: {
    width: "420px",
    height: "450px",
    border: "1px solid #ccc",
    margin: "20px auto",
    display: "flex",
    flexDirection: "column",
    padding: "10px",
    overflowY: "auto",
    borderRadius: "10px",
    background: "#111827",
  },
  message: {
    padding: "10px",
    margin: "6px",
    borderRadius: "12px",
    color: "white",
    maxWidth: "70%",
  },
  inputArea: {
    display: "flex",
    justifyContent: "center",
  },
  input: {
    width: "260px",
    padding: "10px",
    borderRadius: "6px",
    border: "1px solid #ccc",
  },
  button: {
    padding: "10px",
    marginLeft: "5px",
    background: "#3b82f6",
    border: "none",
    color: "white",
    cursor: "pointer",
    borderRadius: "6px",
  },
};

export default App;