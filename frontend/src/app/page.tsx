'use client';

import { useState, useEffect, useCallback } from 'react';

export default function Home() {
  const [users, setUsers] = useState<any[]>([]);
  const [selectedUser, setSelectedUser] = useState<number | null>(null);
  const [tasks, setTasks] = useState<any[]>([]);
  const [health, setHealth] = useState<any[]>([]);
  const [facts, setFacts] = useState<any[]>([]);

  // Form states
  const [newTask, setNewTask] = useState({ 
    title: '', 
    description: '', 
    schedule: '', 
    recurrence: 'daily',
    recurrence_interval: 1,
    recurrence_unit: 'days'
  });
  const [newFact, setNewFact] = useState({ fact: '', category: 'General' });
  const [newHealth, setNewHealth] = useState({ condition: '', status: 'active' });

  const fetchData = useCallback(() => {
    if (!selectedUser) return;
    
    fetch(`http://localhost:8000/api/tasks/${selectedUser}`)
      .then(res => res.json())
      .then(data => setTasks(data));
    
    fetch(`http://localhost:8000/api/health/${selectedUser}`)
      .then(res => res.json())
      .then(data => setHealth(data));
    
    fetch(`http://localhost:8000/api/facts/${selectedUser}`)
      .then(res => res.json())
      .then(data => setFacts(data));
  }, [selectedUser]);

  useEffect(() => {
    fetch('http://localhost:8000/api/users')
      .then(res => res.json())
      .then(data => setUsers(data))
      .catch(err => console.error(err));
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Actions
  const addTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedUser || !newTask.title) return;
    await fetch('http://localhost:8000/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        ...newTask, 
        user_id: selectedUser, 
        schedule: newTask.schedule || null,
        recurrence_interval: Number(newTask.recurrence_interval)
      })
    });
    setNewTask({ 
      title: '', 
      description: '', 
      schedule: '', 
      recurrence: 'daily', 
      recurrence_interval: 1, 
      recurrence_unit: 'days' 
    });
    fetchData();
  };

  const addFact = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedUser || !newFact.fact) return;
    await fetch('http://localhost:8000/api/facts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...newFact, user_id: selectedUser })
    });
    setNewFact({ fact: '', category: 'General' });
    fetchData();
  };

  const addHealth = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedUser || !newHealth.condition) return;
    await fetch('http://localhost:8000/api/health', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...newHealth, user_id: selectedUser })
    });
    setNewHealth({ condition: '', status: 'active' });
    fetchData();
  };

  const deleteTask = async (id: number) => {
    await fetch(`http://localhost:8000/api/tasks/${id}`, { method: 'DELETE' });
    fetchData();
  };

  const deleteFact = async (id: number) => {
    await fetch(`http://localhost:8000/api/facts/${id}`, { method: 'DELETE' });
    fetchData();
  };

  const deleteHealth = async (id: number) => {
    await fetch(`http://localhost:8000/api/health/${id}`, { method: 'DELETE' });
    fetchData();
  };

  const toggleTask = async (task: any) => {
    const newStatus = task.status === 'completed' ? 'pending' : 'completed';
    await fetch(`http://localhost:8000/api/tasks/${task.id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    });
    fetchData();
  };

  return (
    <main className="min-h-screen p-8 bg-slate-50 text-slate-900 font-sans">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight">LifeOS Management</h1>
          <div className="flex gap-2 items-center text-sm font-medium text-slate-500 bg-white px-4 py-2 rounded-full border border-slate-200 shadow-sm">
            <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></span>
            System Online
          </div>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* User Sidebar */}
          <div className="lg:col-span-1 space-y-6">
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
              <h2 className="text-lg font-bold mb-4 text-slate-800">Users</h2>
              <div className="space-y-2">
                {users.length === 0 && <p className="text-sm text-slate-400">No users found. Message the bot first.</p>}
                {users.map(user => (
                  <button
                    key={user.id}
                    onClick={() => setSelectedUser(user.id)}
                    className={`w-full text-left p-3 rounded-xl transition-all duration-200 font-medium ${
                      selectedUser === user.id 
                        ? 'bg-blue-600 text-white shadow-md shadow-blue-200 translate-x-1' 
                        : 'bg-slate-50 text-slate-600 hover:bg-white hover:shadow-sm hover:border-slate-300 border border-transparent'
                    }`}
                  >
                    Chat ID: {user.telegram_chat_id}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3 space-y-8">
            {!selectedUser ? (
              <div className="bg-white p-16 rounded-3xl shadow-sm border border-slate-200 text-center flex flex-col items-center justify-center">
                <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mb-4">
                  <span className="text-3xl">👤</span>
                </div>
                <h3 className="text-xl font-bold text-slate-800 mb-2">Select a User</h3>
                <p className="text-slate-500 max-w-xs mx-auto">Please choose a user from the sidebar to manage their LifeOS memory and daily routines.</p>
              </div>
            ) : (
              <>
                {/* Tasks section */}
                <section className="bg-white p-8 rounded-3xl shadow-sm border border-slate-200">
                  <div className="flex items-center justify-between mb-6">
                    <h2 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
                      <span className="text-blue-600">📋</span> Tasks
                    </h2>
                  </div>
                  
                  <form onSubmit={addTask} className="mb-8 grid grid-cols-1 gap-4 bg-slate-50 p-6 rounded-2xl border border-slate-100">
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div className="space-y-1">
                        <label className="text-xs font-bold text-slate-500 uppercase ml-1">Task Title</label>
                        <input 
                          className="w-full p-3 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all" 
                          placeholder="What needs to be done?" 
                          value={newTask.title} 
                          onChange={e => setNewTask({...newTask, title: e.target.value})} 
                        />
                      </div>
                      <div className="space-y-1">
                        <label className="text-xs font-bold text-slate-500 uppercase ml-1">First Execution</label>
                        <input 
                          className="w-full p-3 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all" 
                          type="datetime-local" 
                          value={newTask.schedule} 
                          onChange={e => setNewTask({...newTask, schedule: e.target.value})} 
                        />
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 items-end">
                      <div className="space-y-1">
                        <label className="text-xs font-bold text-slate-500 uppercase ml-1">Repeat Type</label>
                        <select 
                          className="w-full p-3 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                          value={newTask.recurrence}
                          onChange={e => setNewTask({...newTask, recurrence: e.target.value})}
                        >
                          <option value="daily">Recurring</option>
                          <option value="none">No Recurrence</option>
                        </select>
                      </div>
                      
                      {newTask.recurrence !== 'none' && (
                        <>
                          <div className="space-y-1">
                            <label className="text-xs font-bold text-slate-500 uppercase ml-1">Every</label>
                            <input 
                              type="number"
                              className="w-full p-3 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                              placeholder="1"
                              value={newTask.recurrence_interval}
                              onChange={e => setNewTask({...newTask, recurrence_interval: parseInt(e.target.value)})}
                            />
                          </div>
                          <div className="space-y-1">
                            <label className="text-xs font-bold text-slate-500 uppercase ml-1">Unit</label>
                            <select 
                              className="w-full p-3 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                              value={newTask.recurrence_unit}
                              onChange={e => setNewTask({...newTask, recurrence_unit: e.target.value})}
                            >
                              <option value="hours">Hours</option>
                              <option value="days">Days</option>
                              <option value="weeks">Weeks</option>
                            </select>
                          </div>
                        </>
                      )}
                    </div>
                    
                    <button className="bg-blue-600 text-white p-4 rounded-xl hover:bg-blue-700 w-full font-bold shadow-lg shadow-blue-100 transition-all active:scale-[0.99] mt-2">
                      Create New Task
                    </button>
                  </form>

                  <div className="grid grid-cols-1 gap-4">
                    {tasks.length === 0 && <p className="text-center py-8 text-slate-400 bg-slate-50 rounded-2xl border-2 border-dashed">No tasks listed yet.</p>}
                    {tasks.map(task => (
                      <div key={task.id} className="group flex justify-between items-center p-5 bg-white rounded-2xl border border-slate-100 hover:border-blue-200 hover:shadow-md transition-all">
                        <div className="flex gap-4 items-center">
                          <button 
                            onClick={() => toggleTask(task)}
                            className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all ${
                              task.status === 'completed' ? 'bg-emerald-500 border-emerald-500 text-white' : 'border-slate-300 text-transparent hover:border-emerald-500'
                            }`}
                          >
                            ✓
                          </button>
                          <div>
                            <h3 className={`font-bold text-lg ${task.status === 'completed' ? 'line-through text-slate-400' : 'text-slate-800'}`}>
                              {task.title}
                            </h3>
                            <div className="flex items-center gap-3 mt-1">
                              <span className={`px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-wider ${
                                task.status === 'pending' ? 'bg-amber-100 text-amber-700' : 
                                task.status === 'completed' ? 'bg-emerald-100 text-emerald-700' : 'bg-blue-100 text-blue-700'
                              }`}>
                                {task.status}
                              </span>
                              {task.recurrence !== 'none' && (
                                <span className="text-xs text-slate-500 flex items-center gap-1">
                                  🔄 Every {task.recurrence_interval} {task.recurrence_unit}
                                </span>
                              )}
                              {task.schedule && (
                                <span className="text-xs text-slate-400">
                                  ⏰ {new Date(task.schedule).toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'short' })}
                                </span>
                              )}
                            </div>
                          </div>
                        </div>
                        <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                          <button onClick={() => deleteTask(task.id)} className="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors">
                            🗑️
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </section>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  {/* Health section */}
                  <section className="bg-white p-8 rounded-3xl shadow-sm border border-slate-200">
                    <h2 className="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-2">
                      <span className="text-rose-600">🌡️</span> Health
                    </h2>
                    
                    <form onSubmit={addHealth} className="mb-6 flex gap-2">
                      <input 
                        className="flex-grow p-3 bg-slate-50 border border-slate-100 rounded-xl focus:ring-2 focus:ring-rose-500 outline-none transition-all" 
                        placeholder="Log condition..." 
                        value={newHealth.condition} 
                        onChange={e => setNewHealth({...newHealth, condition: e.target.value})} 
                      />
                      <button className="bg-rose-600 text-white px-4 rounded-xl hover:bg-rose-700 font-bold shadow-md shadow-rose-100">+</button>
                    </form>

                    <div className="space-y-3">
                      {health.map(h => (
                        <div key={h.id} className="flex justify-between items-center p-4 bg-rose-50/50 rounded-2xl border border-rose-100">
                          <div>
                            <h3 className="font-bold text-slate-800">{h.condition}</h3>
                            <p className="text-rose-700 text-xs font-medium uppercase tracking-wider">{h.status}</p>
                          </div>
                          <button onClick={() => deleteHealth(h.id)} className="text-rose-300 hover:text-rose-600 transition-colors">✕</button>
                        </div>
                      ))}
                    </div>
                  </section>

                  {/* Facts section */}
                  <section className="bg-white p-8 rounded-3xl shadow-sm border border-slate-200">
                    <h2 className="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-2">
                      <span className="text-emerald-600">🧠</span> Facts
                    </h2>
                    
                    <form onSubmit={addFact} className="mb-6 flex gap-2">
                      <input 
                        className="flex-grow p-3 bg-slate-50 border border-slate-100 rounded-xl focus:ring-2 focus:ring-emerald-500 outline-none transition-all" 
                        placeholder="New memory..." 
                        value={newFact.fact} 
                        onChange={e => setNewFact({...newFact, fact: e.target.value})} 
                      />
                      <button className="bg-emerald-600 text-white px-4 rounded-xl hover:bg-emerald-700 font-bold shadow-md shadow-emerald-100">+</button>
                    </form>

                    <div className="flex flex-wrap gap-2">
                      {facts.map(f => (
                        <div key={f.id} className="group relative flex items-center px-4 py-2 bg-emerald-50 text-emerald-800 border border-emerald-100 rounded-2xl text-sm font-semibold hover:bg-emerald-100 transition-colors">
                          {f.fact}
                          <button onClick={() => deleteFact(f.id)} className="ml-2 hidden group-hover:inline-block text-rose-500 font-black">×</button>
                        </div>
                      ))}
                    </div>
                  </section>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
