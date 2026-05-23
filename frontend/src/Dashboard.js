import React, { useState, useEffect, useRef } from 'react';
import { Shield, AlertTriangle, Activity, List, ShieldAlert, Info } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const Dashboard = () => {
  const [events, setEvents] = useState([]);
  const [stats, setStats] = useState({ total_packets: 0, total_threats: 0, severity_counts: { LOW: 0, MEDIUM: 0, HIGH: 0, CRITICAL: 0 } });
  const [wsStatus, setWsStatus] = useState('Disconnected');
  const scrollRef = useRef(null);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws');
    
    ws.onopen = () => setWsStatus('Connected');
    ws.onclose = () => setWsStatus('Disconnected');
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setEvents(prev => [data, ...prev].slice(0, 50));
      updateStats(data);
    };

    return () => ws.close();
  }, []);

  const updateStats = (event) => {
    setStats(prev => {
      const newStats = { ...prev };
      newStats.total_packets += 1;
      if (event.prediction === 'ATTACK') {
        newStats.total_threats += 1;
        newStats.severity_counts[event.severity] += 1;
      }
      return newStats;
    });
  };

  return (
    <div className="min-h-screen bg-[#0a0a0c] text-slate-200 p-6 font-mono">
      {/* Header */}
      <header className="flex justify-between items-center mb-8 border-b border-slate-800 pb-4">
        <div className="flex items-center gap-3">
          <Shield className="text-cyan-400 w-8 h-8" />
          <h1 className="text-2xl font-bold tracking-tighter text-white">AI NETWORK THREAT INTELLIGENCE</h1>
        </div>
        <div className={`flex items-center gap-2 px-3 py-1 rounded-full text-xs ${wsStatus === 'Connected' ? 'bg-green-500/10 text-green-400 border border-green-500/20' : 'bg-red-500/10 text-red-400 border border-red-500/20'}`}>
          <div className={`w-2 h-2 rounded-full ${wsStatus === 'Connected' ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
          {wsStatus}
        </div>
      </header>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <StatCard title="Total Packets" value={stats.total_packets} icon={<Activity className="text-blue-400" />} />
        <StatCard title="Threats Detected" value={stats.total_threats} icon={<ShieldAlert className="text-red-400" />} />
        <StatCard title="High/Critical" value={stats.severity_counts.HIGH + stats.severity_counts.CRITICAL} icon={<AlertTriangle className="text-orange-400" />} />
        <StatCard title="System Status" value="SECURE" icon={<Shield className="text-green-400" />} color="text-green-400" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Live Feed */}
        <div className="lg:col-span-2 bg-[#111114] border border-slate-800 rounded-xl overflow-hidden flex flex-col h-[600px]">
          <div className="p-4 border-b border-slate-800 flex justify-between items-center bg-[#16161a]">
            <div className="flex items-center gap-2">
              <List className="w-4 h-4 text-cyan-400" />
              <span className="text-sm font-semibold uppercase tracking-widest">Real-Time Threat Feed</span>
            </div>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-2" ref={scrollRef}>
            {events.map((event, i) => (
              <EventItem key={i} event={event} />
            ))}
          </div>
        </div>

        {/* Sidebar Analytics */}
        <div className="space-y-6">
          <div className="bg-[#111114] border border-slate-800 rounded-xl p-4">
            <h3 className="text-xs font-bold uppercase tracking-widest mb-4 text-slate-500">Severity Distribution</h3>
            <div className="h-48">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={events.slice(0, 10).reverse()}>
                        <Line type="monotone" dataKey="probability" stroke="#22d3ee" strokeWidth={2} dot={false} />
                        <XAxis hide />
                        <YAxis hide domain={[0, 1]} />
                    </LineChart>
                </ResponsiveContainer>
            </div>
          </div>

          <div className="bg-[#111114] border border-slate-800 rounded-xl p-4">
            <h3 className="text-xs font-bold uppercase tracking-widest mb-4 text-slate-500">System Logs</h3>
            <div className="text-[10px] text-slate-500 space-y-1">
              <div>[INFO] AI Model v2.4 initialized.</div>
              <div>[INFO] Scapy sniffer started on interface eth0.</div>
              <div>[WARN] High traffic volume detected from 192.168.1.1.</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ title, value, icon, color = "text-white" }) => (
  <div className="bg-[#111114] border border-slate-800 p-4 rounded-xl flex items-center justify-between">
    <div>
      <p className="text-[10px] uppercase tracking-widest text-slate-500 mb-1">{title}</p>
      <p className={`text-2xl font-bold ${color}`}>{value}</p>
    </div>
    <div className="bg-slate-800/50 p-2 rounded-lg">{icon}</div>
  </div>
);

const EventItem = ({ event }) => {
  const isAttack = event.prediction === 'ATTACK';
  const severityColors = {
    LOW: 'text-blue-400',
    MEDIUM: 'text-yellow-400',
    HIGH: 'text-orange-400',
    CRITICAL: 'text-red-500'
  };

  return (
    <div className={`p-3 rounded-lg border ${isAttack ? 'bg-red-500/5 border-red-500/20' : 'bg-slate-800/10 border-slate-800'} flex items-center justify-between group transition-all hover:bg-slate-800/30`}>
      <div className="flex items-center gap-4">
        <span className="text-[10px] text-slate-500 w-16">{event.timestamp}</span>
        <div>
          <div className="flex items-center gap-2">
            <span className={`text-xs font-bold ${isAttack ? 'text-red-400' : 'text-green-400'}`}>
              {event.attack_type}
            </span>
            <span className={`text-[10px] px-1.5 py-0.5 rounded border ${isAttack ? 'border-red-500/30 bg-red-500/10' : 'border-slate-700 bg-slate-800'} ${severityColors[event.severity]}`}>
              {event.severity}
            </span>
          </div>
          <div className="text-[11px] text-slate-400 mt-0.5">
            {event.src} -> {event.dst} ({event.proto})
          </div>
        </div>
      </div>
      <div className="flex items-center gap-3">
        <div className="text-right">
            <div className="text-[10px] text-slate-500 uppercase">Confidence</div>
            <div className="text-xs font-bold text-cyan-400">{(event.probability * 100).toFixed(1)}%</div>
        </div>
        <button className="opacity-0 group-hover:opacity-100 p-1.5 bg-slate-800 rounded-md hover:bg-slate-700 transition-all">
          <Info className="w-3.5 h-3.5 text-slate-400" />
        </button>
      </div>
    </div>
  );
};

export default Dashboard;
