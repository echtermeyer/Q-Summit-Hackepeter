export const initialNodes = [
    {
      id: '1',
      data: { label: 'ROOT' },
      position: { x: 0, y: 0 },
    },
    {
      id: '2',
      data: { label: 'node 2' },
      position: { x: 0, y: 0 },
    },
    {
      id: '2a',
      data: { label: 'node 2a' },
      position: { x: 0, y: 0 },
    },
    {
      id: '2b',
      data: { label: 'node 2b' },
      position: { x: 0, y: 0 },
    },
    {
      id: '2c',
      data: { label: 'node 2c' },
      position: { x: 0, y: 0 },
    },
    {
      id: '3',
      data: { label: 'node 3' },
      position: { x: 0, y: 0 },
    },
    {
        id: '3b',
        data: { label: 'node 3b' },
        position: { x: 0, y: 0 },
    },
    {
    id: '4',
    data: { label: 'node 4' },
    position: { x: 0, y: 0 },
    },
    {
        id: '4b',
        data: { label: 'node 4b' },
        position: { x: 0, y: 0 },
    },

  ];
  
  export const initialEdges = [
    { id: 'e12', source: '1', target: '2', animated: false },
    { id: 'e13', source: '1', target: '3', animated: false },
    { id: 'e22a', source: '2', target: '2a', animated: false },
    { id: 'e22b', source: '2', target: '2b', animated: false },
    { id: 'e22c', source: '2', target: '2c', animated: false },
    { id: 'e33b', source: '3', target: '3b', animated: false },
    { id: 'e14', source: '1', target: '4', animated: false },
    { id: 'e14b', source: '4', target: '4b', animated: false },
  ];
  