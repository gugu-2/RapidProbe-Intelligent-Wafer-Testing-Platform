import React, { useEffect, useState } from 'react';
import { fetchWaferMap } from '../api';

export default function WaferMap({ waferId }) {
  const [map, setMap] = useState([]);
  useEffect(() => { fetchWaferMap(waferId).then(res => setMap(res.die_data)); }, [waferId]);
  return (
    <svg width="400" height="400">
      {map.map((d, i) => (
        <rect key={i} x={d.x*20} y={d.y*20} width="18" height="18"
          fill={d.status === 'pass' ? 'green' : 'red'} />
      ))}
    </svg>
  );
}
