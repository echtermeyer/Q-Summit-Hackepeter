// Home.jsx (für React Router v6)
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";
import {
  Card,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Minus, Plus } from "lucide-react";
import { Bar, BarChart, ResponsiveContainer } from "recharts";

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

import "./Home.css";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";

import Typewriter from "typewriter-effect";

import Lottie from "react-lottie";
import lottiGlobe from "../assets/lotti_globe.json";

const defaultOptions = {
  loop: true,
  autoplay: true,
  animationData: lottiGlobe,
};

const data = [
  {
    goal: 100,
  },
  {
    goal: 110,
  },
  {
    goal: 121,
  },
  {
    goal: 133,
  },
  {
    goal: 145,
  },
  {
    goal: 162,
  },
  {
    goal: 180,
  },
  {
    goal: 199,
  },
  {
    goal: 232,
  },
  {
    goal: 270,
  },
  {
    goal: 301,
  },
  {
    goal: 350,
  },
  {
    goal: 411,
  },
];

const Home = () => {
  const navigate = useNavigate();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [topic, setTopic] = useState("");

  const reduceEmissions = async () => {
    // Definiere den Request-Body
    const requestBody = {
      sector: topic
    };
    //console.log(requestBody)
    // Navigiere sofort zur "/main"-Seite
    navigate("/main");
  
    try {
      // Sende einen POST-Request ohne auf die Antwort zu warten
      fetch('http://localhost:8000/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      })
      .then(response => {
        if (!response.ok) {
          // Handle Fehler, wenn der Request nicht erfolgreich war
          console.error('Failed to start the process', response.statusText);
        }
      })
      .catch(error => {
        // Fange Netzwerkfehler ab
        console.error('Network error:', error);
      });
    } catch (error) {
      // Fange Fehler beim Senden des Requests ab
      console.error('Error sending the request:', error);
    }
  };
  
  const handleInputChange = (e) => {
    setTopic(e.target.value); // Setze 'topic' auf den Wert des Input-Felds
  };
  
  const toggleSidebar = () => setIsSidebarOpen(!isSidebarOpen);

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <div className="flex-grow overflow-auto">
        <div className="flexContainer minusMargin">
          <div className="firstColumn">
            <Lottie options={defaultOptions} height={500} width={500} />
          </div>
          <div className="secondColumn">
            <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl">
              <Typewriter
                options={{
                  strings: [
                    "Evidence-based emissions advisor for a sustainable future!",
                  ],
                  autoStart: true,
                  loop: true,
                  deleteSpeed: 10,
                }}
              />
            </h1>
          </div>
        </div>

        <div className="flex justify-center items-center customMargin flexedBackground">
          <div className="w-[70vw]">
            <Card>
              <CardHeader>
                <CardTitle>Analyse sector</CardTitle>
                <CardDescription>
                  Specify a sector of your interest to find insights and reduce
                  emissions
                </CardDescription>
              </CardHeader>
              <CardFooter className="flex justify-between">
                <Input className="mr-6" placeholder="Your public section" value={topic} onChange={handleInputChange}/>
                <Button onClick={reduceEmissions}>Reduce Emissions</Button>
              </CardFooter>
            </Card>
          </div>
        </div>

        <div className="flexContainer">
          <div className="firstColumn">
            <Accordion type="single" collapsible className="w-full">
              <AccordionItem value="item-1">
                <AccordionTrigger>What data is used?</AccordionTrigger>
                <AccordionContent>
                  Our data-driven approach has access to over 7 million academic
                  papers, 1.5 million patents, and 1.5 million news articles.
                </AccordionContent>
              </AccordionItem>
              <AccordionItem value="item-2">
                <AccordionTrigger>How reliable is our AI?</AccordionTrigger>
                <AccordionContent>
                  Thanks to our state-of-the-art machine learning models and
                  grounding in scientific literature, our AI is highly reliable.
                  Nevertheless, we always recommend to consult with domain
                  experts.
                </AccordionContent>
              </AccordionItem>
              <AccordionItem value="item-3">
                <AccordionTrigger>
                  Which decisions are supported?
                </AccordionTrigger>
                <AccordionContent>
                  Our AI supports decisions in various sectors, such as energy,
                  agriculture, and transportation. It can help you reduce
                  emissions, optimize processes, and much more.
                </AccordionContent>
              </AccordionItem>
            </Accordion>
          </div>
          <div className="secondColumn">
            <div className="mx-auto w-full max-w-sm">
              <h2 className="text-xl font-bold text-center my-2">
                Reduced CO2 emissions (t)
              </h2>
              <p className="text-center text-sm mb-4">
                Evidence-based decision support provided by our AI help reducing
                CO2 emissions drastically
              </p>

              <div className="h-[20vw]">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={data}>
                    <Bar
                      dataKey="goal"
                      style={
                        {
                          fill: "hsl(var(--foreground))",
                          opacity: 0.9,
                        } as React.CSSProperties
                      }
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        </div>
        <Separator className="my-4" />

        <div className="flex justify-center items-center customMargin flexedBackground2"></div>
      </div>
    </div>
  );
};

export default Home;
