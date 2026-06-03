'use client';

import { useState, useEffect, useCallback } from 'react';

export default function Home() {
  const [users, setUsers] = useState<any[]>([]);
  const [selectedUser, setSelectedUser] = useState<number | null>(null);
  const [tasks, setTasks] = useState<any[]>([]);
  const [health, setHealth] = useState<any[]>([]);
  const [facts, setFacts] = useState<any[]>([]);

  // Form states
  const [newTask, setNewTask] = useState({ title: '', description: '', schedule: '' });
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
      body: JSON.stringify({ ...newTask, user_id: selectedUser, schedule: newTask.schedule || null })
    });
    setNewTask({ title: '', description: '', schedule: '' });
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
    <main className="min-h-screen p-8 bg-slate-50 text-slate-900">
      <h1 className="text-4xl font-bold mb-8 text-slate-900">LifeOS Management</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {/* User Sidebar */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 h-fit">
          <h2 className="text-xl font-semibold mb-4">Users</h2>
          <div className="space-y-2">
            {users.map(user => (
              <button
                key={user.id}
                onClick={() => setSelectedUser(user.id)}
                className={`w-full text-left p-3 rounded-lg transition-colors ${
                  selectedUser === user.id ? 'bg-blue-600 text-white' : 'hover:bg-slate-100'
                }`}
              >
                Chat ID: {user.telegram_chat_id}
              </button>
            ))}
          </div>
        </div>

        {/* Main Content */}
        <div className="md:col-span-3 space-y-8">
          {!selectedUser ? (
            <div className="bg-white p-12 rounded-xl shadow-sm border border-slate-200 text-center">
              <p className="text-slate-500 text-lg">Select a user to manage their LifeOS data.</p>
            </div>
          ) : (
            <>
              {/* Tasks section */}
              <section className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                <h2 className="text-2xl font-bold mb-4 text-blue-700">Tasks</h2>
                
                <form onSubmit={addTask} className="mb-6 grid grid-cols-1 sm:grid-cols-3 gap-2 bg-slate-50 p-4 rounded-lg">
                  <input 
                    className="p-2 border rounded" 
                    placeholder="Task Title" 
                    value={newTask.title} 
                    onChange={e => setNewTask({...newTask, title: e.target.value})} 
                  />
                  <input 
                    className="p-2 border rounded" 
                    type="datetime-local" 
                    value={newTask.schedule} 
                    onChange={e => setNewTask({...newTask, schedule: e.target.value})} 
                  />
                  <button className="bg-blue-600 text-white p-2 rounded hover:bg-blue-700">Add Task</button>
                </form>

                <div className="grid grid-cols-1 gap-4">
                  {tasks.map(task => (
                    <div key={task.id} className="flex justify-between items-center p-4 bg-slate-50 rounded-lg border border-slate-100">
                      <div>
                        <h3 className={`font-semibold text-lg ${task.status === 'completed' ? 'line-through text-slate-400' : ''}`}>
                          {task.title}
                        </h3>
                        <p className="text-slate-600 text-sm">{task.status}</p>
                        {task.schedule && <p className="text-xs text-slate-400">{new Date(task.schedule).toLocaleString()}</p>}
                      </div>
                      <div className="flex gap-2">
                        <button onClick={() => toggleTask(task)} className="p-2 text-blue-600 hover:bg-blue-50 rounded">
                          {task.status === 'completed' ? 'Undo' : 'Done'}
                        </button>
                        <button onClick={() => deleteTask(task.id)} className="p-2 text-red-600 hover:bg-red-50 rounded">Delete</button>
                      </div>
                    </div>
                  ))}
                </div>
              </section>

              {/* Health section */}
              <section className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                <h2 className="text-2xl font-bold mb-4 text-red-600">Health Records</h2>
                
                <form onSubmit={addHealth} className="mb-6 flex gap-2 bg-red-50 p-4 rounded-lg">
                  <input 
                    className="flex-grow p-2 border rounded" 
                    placeholder="Condition (e.g. Fever)" 
                    value={newHealth.condition} 
                    onChange={e => setNewHealth({...newHealth, condition: e.target.value})} 
                  />
                  <button className="bg-red-600 text-white p-2 rounded hover:bg-red-700">Add Record</button>
                </form>

                <div className="space-y-3">
                  {health.map(h => (
                    <div key={h.id} className="flex justify-between items-center p-4 bg-red-50 rounded-lg border border-red-100">
                      <div>
                        <h3 className="font-semibold">{h.condition}</h3>
                        <p className="text-red-700 text-sm">{h.status}</p>
                      </div>
                      <button onClick={() => deleteHealth(h.id)} className="p-2 text-red-600 hover:bg-red-100 rounded">Delete</button>
                    </div>
                  ))}
                </div>
              </section>

              {/* Facts section */}
              <section className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                <h2 className="text-2xl font-bold mb-4 text-emerald-600">Life Facts</h2>
                
                <form onSubmit={addFact} className="mb-6 flex gap-2 bg-emerald-50 p-4 rounded-lg">
                  <input 
                    className="flex-grow p-2 border rounded" 
                    placeholder="New Life Fact..." 
                    value={newFact.fact} 
                    onChange={e => setNewFact({...newFact, fact: e.target.value})} 
                  />
                  <button className="bg-emerald-600 text-white p-2 rounded hover:bg-emerald-700">Add Fact</button>
                </form>

                <div className="flex flex-wrap gap-2">
                  {facts.map(f => (
                    <div key={f.id} className="group relative flex items-center px-3 py-1 bg-emerald-100 text-emerald-800 rounded-full text-sm font-medium">
                      {f.fact}
                      <button onClick={() => deleteFact(f.id)} className="ml-2 hidden group-hover:inline-block text-red-600 font-bold">×</button>
                    </div>
                  ))}
                </div>
              </section>
            </>
          )}
        </div>
      </div>
    </main>
  );
}
