import React, { useState, useEffect } from "react";

interface TypewriterProps {
  text: string;
  speed: number;
}

export const Typewriter: React.FC<TypewriterProps> = ({
  text = "Hallo Welt ich bin ein Typewriter!",
  speed = 100,
}) => {
  const [typedText, setTypedText] = useState("");

  useEffect(() => {
    if (typedText.length < text.length) {
      const timeoutId = setTimeout(() => {
        setTypedText(text.substring(0, typedText.length + 1));
      }, speed);

      return () => clearTimeout(timeoutId);
    }
  }, [typedText, text, speed]);

  return <div>{typedText}</div>;
};
