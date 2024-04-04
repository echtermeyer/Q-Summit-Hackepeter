import ELK from "elkjs/lib/elk.bundled.js";
import React, { useCallback, useEffect, useState } from "react";
import ReactFlow, {
  ReactFlowProvider,
  Panel,
  useNodesState,
  useEdgesState,
  useReactFlow,
  Background,
  Controls,
  MiniMap,
} from "reactflow";
import { Button } from "./ui/button.js";
import Sidebar from "./Sidebar.js";

// import { initialNodes, initialEdges } from './nodes-edges copy.js';
const initialNodes: any[] = [];

const initialEdges: any[] = [];

import "reactflow/dist/style.css";

const elk = new ELK();

const useLayoutedElements = () => {
  const { getNodes, setNodes, getEdges, fitView } = useReactFlow();
  const defaultOptions = {
    "elk.algorithm": "org.eclipse.elk.radia",
    "elk.layered.spacing.nodeNodeBetweenLayers": 100,
    "elk.spacing.nodeNode": 80,
  };

  const getLayoutedElements = useCallback((options: any) => {
    const layoutOptions = { ...defaultOptions, ...options };
    const graph = {
      id: "root",
      layoutOptions: layoutOptions,
      children: getNodes(),
      edges: getEdges(),
    };

    elk.layout(graph).then(({ children }) => {
      // By mutating the children in-place we saves ourselves from creating a
      // needless copy of the nodes array.
      children.forEach((node: { position: { x: any; y: any }; x: any; y: any }) => {
        node.position = { x: node.x, y: node.y };
      });

      setNodes(children);
      window.requestAnimationFrame(() => {
        fitView();
      });
    });
  }, []);

  return { getLayoutedElements };
};

const LayoutFlow = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const { getLayoutedElements } = useLayoutedElements();

  const [layoutUpdateNeeded, setLayoutUpdateNeeded] = useState(false);

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  const handleNodeClick = (event, node) => {
    setSelectedId(Number(node.id));
    toggleSidebar();
  };

  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [isOpen, setIsOpen] = useState<boolean>(false);

  const [data, setData] = useState({
    node: [],
  });

  const addNewContent = (newContentDetails: Content) => {
    setData((prevData: AppState) => {
      const updatedContents = [...prevData.contents, newContentDetails];

      return {
        ...prevData,
        contents: updatedContents,
      };
    });
  };

  const nodeStyles = {
    root: {
      fontWeight: "bold",
      borderWidth: "2px", // Specify a custom border width that is less thick
    },
    area: {
      fontWeight: "bold",
    },
  };

  useEffect(() => {
    setNodes([]);
    setEdges([]);

  }, [setNodes, setEdges]);

  useEffect(() => {
    const intervalId = setInterval(() => {
      fetch("http://localhost:8000/graph")
        .then((response) => response.json())
        .then((data) => {
          const currentLength = nodes.length;
          const newNodes = data.node.filter((node: { id: number }) => node.id > currentLength);
          const formattedNewNodes = newNodes.map((node: { id: any; name: any }) => ({
            id: String(node.id),
            data: { label: node.name },
            position: { x: 0, y: 0 },
            style: nodeStyles[node.type] || {},
          }));
          setData(data);
          //console.log(data);

          let updatesMade = false; // Flag to check if any updates were made

          // Update nodes if new ones are found
          if (formattedNewNodes.length > 0) {
            setNodes((currentNodes) => [...currentNodes, ...formattedNewNodes]);
            updatesMade = true; // Set updates flag to true
          }

          // Update edges based on new nodes
          const newEdges = newNodes
            .filter((node: { parent_id: null }) => node.parent_id !== null)
            .map((node: { parent_id: any; id: any }) => ({
              id: `e${node.parent_id}-${node.id}`,
              source: String(node.parent_id),
              target: String(node.id),
              animated: false,
            }));

          // Update edges if new ones are found
          if (newEdges.length > 0) {
            setEdges((currentEdges) => [...currentEdges, ...newEdges]);
            console.log("Adding new edges:", newEdges);
            updatesMade = true; // Set updates flag to true (redundant if new nodes always lead to new edges, but necessary if that's not always the case)
          }

          // Trigger layout update if any updates were made
          if (updatesMade) {
            setLayoutUpdateNeeded(true);
          }
        })
        .catch((error) => console.error("Failed to fetch new nodes:", error));
    }, 1000);

    return () => clearInterval(intervalId);
  }, [nodes, setNodes, edges, setEdges, setLayoutUpdateNeeded]);

  useEffect(() => {
    if (layoutUpdateNeeded) {
      getLayoutedElements({
        "elk.algorithm": "org.eclipse.elk.radial",
      });
      // Reset the flag to avoid repeated layout updates
      setLayoutUpdateNeeded(false);
    }
  }, [layoutUpdateNeeded, getLayoutedElements]);

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <div style={{ width: isOpen ? "0" : "0", transition: "width 0.3s" }}>
        <Sidebar selectedId={selectedId} isOpen={isOpen} toggleSidebar={toggleSidebar} contents={data.node} />
      </div>
      <div style={{ flex: 1 }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodeClick={handleNodeClick}
          fitView={true}
        >
          <Background />
          <MiniMap />
          <Controls />
          <Panel position="top-right">
            <Button
              onClick={() =>
                getLayoutedElements({
                  "elk.algorithm": "org.eclipse.elk.radial",
                })
              }
            >
              radial layout
            </Button>
          </Panel>
        </ReactFlow>
      </div>
    </div>
  );
};

const LayoutFlowComponent = () => {
  return (
    <ReactFlowProvider>
      <LayoutFlow className="layoutFlow" />
    </ReactFlowProvider>
  );
};

export default LayoutFlowComponent;
