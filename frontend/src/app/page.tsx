'use client';

import { useState, useEffect } from 'react';

export default function Home() {
  const [users, setUsers] = useState<any[]>([]);
  const [selectedUser, setSelectedUser] = useState<number | null>(null);
  const [tasks, setTasks] = useState<any[]>([]);
  const [health, setHealth] = useState<any[]>([]);
  const [facts, setFacts] = useState<any[]>([]);

  useEffect(() => {
    fetch('http://localhost:8000/api/users')
      .then(res => res.json())
      .then(data => setUsers(data))
      .catch(err => console.error(err));
  }, []);

  useEffect(() => {
    if (selectedUser) {
      fetch(`http://localhost:8000/api/tasks/${selectedUser}`)
        .then(res => res.json())
        .then(data => setTasks(data));
      
      fetch(`http://localhost:8000/api/health/${selectedUser}`)
        .then(res => res.json())
        .then(data => setHealth(data));
      
      fetch(`http://localhost:8000/api/facts/${selectedUser}`)
        .then(res => res.json())
        .then(data => setFacts(data));
    }
  }, [selectedUser]);

  return (
    <main className="min-h-screen p-8 bg-slate-50">
      <h1 className="text-4xl font-bold mb-8 text-slate-900">LifeOS Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {/* User Sidebar */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
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
        <div className="md:col-span-3 space-y-6">
          {!selectedUser ? (
            <div className="bg-white p-12 rounded-xl shadow-sm border border-slate-200 text-center">
              <p className="text-slate-500 text-lg">Select a user to view their LifeOS memory.</p>
            </div>
          ) : (
            <>
              {/* Tasks section */}
              <section className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                <h2 className="text-2xl font-bold mb-4 text-blue-700">Tasks</h2>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {tasks.map(task => (
                    <div key={task.id} className="p-4 bg-slate-50 rounded-lg border border-slate-100">
                      <h3 className="font-semibold text-lg">{task.title}</h3>
                      <p className="text-slate-600 text-sm">{task.status}</p>
                      {task.schedule && <p className="text-xs text-slate-400 mt-2">{new Date(task.schedule).toLocaleString()}</p>}
                    </div>
                  ))}
                </div>
              </section>

              {/* Health section */}
              <section className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                <h2 className="text-2xl font-bold mb-4 text-red-600">Health Records</h2>
                <div className="space-y-3">
                  {health.map(h => (
                    <div key={h.id} className="p-4 bg-red-50 rounded-lg border border-red-100">
                      <h3 className="font-semibold">{h.condition}</h3>
                      <p className="text-red-700 text-sm">{h.status}</p>
                    </div>
                  ))}
                </div>
              </section>

              {/* Facts section */}
              <section className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                <h2 className="text-2xl font-bold mb-4 text-emerald-600">Life Facts</h2>
                <div className="flex flex-wrap gap-2">
                  {facts.map(f => (
                    <span key={f.id} className="px-3 py-1 bg-emerald-100 text-emerald-800 rounded-full text-sm font-medium">
                      {f.fact}
                    </span>
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
