import React from 'react';
import { Handle, Position } from 'react-flow-renderer';
import './circle_node.css'; // Import your CSS file like this

const CircleNode = ({ data }) => {
  return (
    <div className="circle-node">
      {/* Invisible handles positioned as specified in your CSS */}
      <Handle type="target" position={Position.Top} />
      <Handle type="source" position={Position.Bottom} />
      <div className="circle-content">{data.label}</div>
    </div>
  );
};

export default CircleNode;


// import React from 'react';
// import './circle_node.css'; // Import your CSS file like this

// const CircleNode = ({ data }) => {
//   return (
//     <div className="circle-node">
//       <div className="circle-content">{data.label}</div>
//     </div>
//   );
// };

// export default CircleNode;