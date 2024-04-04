import React, { useEffect, useState } from "react";
import "./Sidebar.css";
import { ScrollArea } from "./ui/scroll-area";
import { Button } from "./ui/button";
import { Progress } from "./ui/progress";
import { Separator } from "./ui/separator";

import { Card, CardContent, CardDescription, CardHeader, CardTitle, ChatWindow } from "@/components/ui/card";

interface Source {
  name: string;
  link: string;
}

interface Metadata {
  description: string;
  science?: string;
  effectiveness: number;
  scientific_concensus?: number;
  realization_speed?: number;
}

// Neues Interface speziell für die Action-Metadaten
interface ActionMetadata extends Metadata {
  sources: Source[]; // Jetzt nur in ActionMetadata enthalten
}

interface BaseContent {
  id: number;
  name: string;
  type: "root" | "area" | "action";
}

interface RootContent extends BaseContent {
  type: "root";
  metadata: Metadata;
}

interface AreaContent extends BaseContent {
  type: "area";
  parent_id: number;
  metadata: Metadata;
}

interface ActionContent extends BaseContent {
  type: "action";
  parent_id: number;
  metadata: ActionMetadata; // Verwendung von ActionMetadata hier
}

type Content = RootContent | AreaContent | ActionContent;

const exampleContent: Content[] = [
  // RootContent und AreaContent haben keine 'sources' mehr in 'metadata'
  {
    id: 1,
    name: "Car Emissions",
    type: "root",
    metadata: {
      description: "Car Emissions 2024",
    },
  },
  {
    id: 2,
    parent_id: 1,
    name: "Transportation",
    type: "area",
    metadata: {
      description: "Lorem Ipsum",
    },
  },
  // ActionContent enthält 'sources' in 'metadata'
  {
    id: 3,
    parent_id: 2,
    name: "Speed Limit",
    type: "action",
    metadata: {
      description: "Lorem Ipsum",
      sources: [
        { name: "Google", link: "https://www.google.de" },
        { name: "Wikipedia", link: "https://www.wikipedia.org" },
      ],
      science: "physics",
      effectiveness: 4,
      scientific_concenus: 1,
      realization_speed: 1,
    },
  },
  {
    id: 4,
    parent_id: 2,
    name: "Higher Taxes",
    type: "action",
    metadata: {
      description: "Lorem Ipsum",
      sources: [{ name: "Government Site", link: "https://www.government.gov" }],
      science: "economics",
      effectiveness: 2,
      scientific_concensus: 0.5,
      realization_speed: 2,
    },
  },
];

interface SidebarProps {
  selectedId: number | null;
  isOpen: boolean;
  toggleSidebar: () => void;
  contents: Content[];
}

const Sidebar: React.FC<SidebarProps> = ({ selectedId, isOpen, toggleSidebar, contents }) => {
  // Find the selected item based on the provided selectedId
  const selectedContent = contents?.find((content) => content.id === selectedId);
  // console.log(contents);
  // console.log(selectedContent);

  return (
    <>
      <div className={`sidebar-container ${isOpen ? "open" : "closed"}`}>
        <div className="sidebar">
          <ScrollArea className="h-[90%] w-[100%] rounded-md overflow-auto" id="scroll-area">
            {selectedContent && (
              <div className="mb-4">
                <Card>
                  <CardHeader>
                    <CardTitle>
                      {selectedContent.name} ({selectedContent.id})
                    </CardTitle>
                    <CardDescription>{selectedContent.type}</CardDescription>
                    <Separator className="my-4" />
                  </CardHeader>
                  <CardContent>
                    <p>{selectedContent.metadata.description}</p>
                    {selectedContent.type === "action" && (
                      <>
                        <Separator className="my-4" />
                        <p>
                          Effectiveness: <Progress value={Number(selectedContent.metadata.metrics.effectiveness)} />
                        </p>
                        <Separator className="my-4" />
                        <p>
                          Scientific Consensus:{" "}
                          <Progress value={Number(selectedContent.metadata.metrics.scientific_concensus)} />
                        </p>
                        <Separator className="my-4" />
                        <p>
                          Realization Speed:{" "}
                          <Progress value={Number(selectedContent.metadata.metrics.realization_speed)} />
                        </p>
                        <Separator className="my-4" />
                        <p>Research Results: {selectedContent.metadata.science}</p>
                        <Separator className="my-4" />
                        <p>References:</p>
                        <ul>
                          {Object.entries(selectedContent.metadata.sources).map(([title, url], index) => (
                            <li key={index}>
                              {url.startsWith("https") ? (
                                <a href={url} style={{ color: "blue", textDecoration: "underline" }}>
                                  {title}
                                </a>
                              ) : (
                                <span>{title}</span>
                              )}
                            </li>
                          ))}
                        </ul>
                      </>
                    )}
                    {selectedContent.type === "area" && (
                      <>
                        <Separator className="my-4" />
                        <p>Actions:</p>
                        <ul>
                          {exampleContent
                            .filter((content) => content.parent_id === selectedContent.id)
                            .map((action) => (
                              <li key={action.id}>
                                {action.id} - {action.name}
                              </li>
                            ))}
                        </ul>
                      </>
                    )}
                  </CardContent>
                </Card>
                <ChatWindow selectedContent={selectedContent} />
              </div>
            )}
          </ScrollArea>
          <Button onClick={() => toggleSidebar()} className="w-[100%] p-2 mt-4">
            Close
          </Button>
        </div>
      </div>
    </>
  );
};

export default Sidebar;
