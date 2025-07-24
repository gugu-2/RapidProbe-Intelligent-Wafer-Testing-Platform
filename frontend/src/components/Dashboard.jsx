import React, { useEffect, useState } from 'react';
import { fetchYieldData } from '../api';
import { LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts';

export default function Dashboard() {
  const [data, setData] = useState([]);
  useEffect(() => {
    fetchYieldData().then(res => setData([{ date: new Date().toISOString(), yield: res.yield }]));
  }, []);
  return (
    <div>
      <h1>Wafer Yield</h1>
      <LineChart width={600} height={300} data={data}>
        <XAxis dataKey="date"/>
        <YAxis unit="%"/>
        <Tooltip/>
        <Line type="monotone" dataKey="yield"/>
      </LineChart>
    </div>
  );
}
