// import React from 'react'
// import ReactDOM from 'react-dom/client'
// import App from '../App.tsx'
import React, { useEffect, useState } from "react";
import "../index.css";
import "./insight.css";
import LayoutFlowComponent from "../components/mindmap";
import Header from "@/components/Header";

const Insight = () => {
  return (
    <div>
      <Header />
      <LayoutFlowComponent />
    </div>
  );
};

export default Insight;
