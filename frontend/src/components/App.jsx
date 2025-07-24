import React, { useEffect, useState } from 'react';
import Login from './Login';
import Dashboard from './Dashboard';

export default function App() {
  const [authed, setAuthed] = useState(false);
  useEffect(() => setAuthed(!!localStorage.getItem('token')), []);
  return authed ? <Dashboard /> : <Login onSuccess={() => setAuthed(true)} />;
}
