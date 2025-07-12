import React, { useState, useEffect, createContext, useContext } from "react";
import "./App.css";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Context for user authentication and global state
const AppContext = createContext();

// Main App Component
function App() {
  const [user, setUser] = useState(null);
  const [currentView, setCurrentView] = useState('home');
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);

  // Mock user for demo (in real app, this would come from authentication)
  useEffect(() => {
    // Demo user setup
    const demoUser = {
      id: 'demo-user-123',
      name: 'John Doe',
      email: 'john@example.com',
      phone: '+1234567890',
      role: 'both',
      rating: 4.8,
      total_reviews: 25,
      location: {
        latitude: 40.7128,
        longitude: -74.0060,
        address: 'New York, NY',
        is_shared: true
      }
    };
    setUser(demoUser);
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API}/tasks`);
      setTasks(response.data);
    } catch (error) {
      console.error('Error loading tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AppContext.Provider value={{ user, setUser, currentView, setCurrentView, tasks, setTasks, loadTasks }}>
      <div className="App min-h-screen bg-gray-50">
        <Header />
        <main className="container mx-auto px-4 py-8">
          {currentView === 'home' && <HomePage />}
          {currentView === 'browse-tasks' && <BrowseTasksPage />}
          {currentView === 'post-task' && <PostTaskPage />}
          {currentView === 'my-tasks' && <MyTasksPage />}
          {currentView === 'profile' && <ProfilePage />}
          {currentView === 'payments' && <PaymentsPage />}
        </main>
        <BottomNavigation />
      </div>
    </AppContext.Provider>
  );
}

// Header Component
const Header = () => {
  const { user, currentView } = useContext(AppContext);

  const getPageTitle = () => {
    switch(currentView) {
      case 'home': return 'TaskMarket';
      case 'browse-tasks': return 'Browse Tasks';
      case 'post-task': return 'Post a Task';
      case 'my-tasks': return 'My Tasks';
      case 'profile': return 'Profile';
      case 'payments': return 'Payments';
      default: return 'TaskMarket';
    }
  };

  return (
    <header className="bg-white shadow-lg">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-blue-600">{getPageTitle()}</h1>
          {user && (
            <div className="flex items-center space-x-3">
              <div className="text-right">
                <p className="text-sm font-medium text-gray-900">{user.name}</p>
                <p className="text-xs text-gray-500">⭐ {user.rating} ({user.total_reviews} reviews)</p>
              </div>
              <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-semibold">
                {user.name.charAt(0)}
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

// Home Page Component
const HomePage = () => {
  const { setCurrentView } = useContext(AppContext);

  const heroImages = [
    "https://images.unsplash.com/photo-1577100078641-e92b0a906760?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzF8MHwxfHNlYXJjaHwyfHxnaWclMjBlY29ub215fGVufDB8fHx8MTc1MjMwODU5MHww&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1715351123666-6a9c4f180c54?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzF8MHwxfHNlYXJjaHwzfHxnaWclMjBlY29ub215fGVufDB8fHx8MTc1MjMwODU5MHww&ixlib=rb-4.1.0&q=85",
    "https://images.pexels.com/photos/8476597/pexels-photo-8476597.jpeg"
  ];

  const serviceCategories = [
    { id: 'delivery', name: 'Delivery & Courier', icon: '🚚', color: 'bg-blue-500' },
    { id: 'cleaning', name: 'Cleaning Services', icon: '🧽', color: 'bg-green-500' },
    { id: 'handyman', name: 'Handyman & Repairs', icon: '🔧', color: 'bg-yellow-500' },
    { id: 'moving', name: 'Moving & Lifting', icon: '📦', color: 'bg-purple-500' },
    { id: 'beauty', name: 'Beauty & Wellness', icon: '💄', color: 'bg-pink-500' },
    { id: 'tech_support', name: 'Tech Support', icon: '💻', color: 'bg-indigo-500' },
    { id: 'tutoring', name: 'Tutoring & Teaching', icon: '📚', color: 'bg-red-500' },
    { id: 'pet_care', name: 'Pet Care', icon: '🐕', color: 'bg-orange-500' },
    { id: 'transportation', name: 'Transportation', icon: '🚗', color: 'bg-teal-500' },
    { id: 'other', name: 'Other Services', icon: '⚡', color: 'bg-gray-500' }
  ];

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl overflow-hidden">
        <div className="absolute inset-0 bg-black opacity-30"></div>
        <div className="relative z-10 px-8 py-16 text-center text-white">
          <h1 className="text-4xl md:text-6xl font-bold mb-4">
            Your All-in-One Task Marketplace
          </h1>
          <p className="text-xl md:text-2xl mb-8">
            Connect with skilled taskers or offer your services to earn money
          </p>
          <div className="flex flex-col md:flex-row gap-4 justify-center">
            <button 
              onClick={() => setCurrentView('browse-tasks')}
              className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100 transition-colors"
            >
              Find Services
            </button>
            <button 
              onClick={() => setCurrentView('post-task')}
              className="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white hover:text-blue-600 transition-colors"
            >
              Post a Task
            </button>
          </div>
        </div>
        <div className="absolute bottom-0 right-0 w-1/3 h-full opacity-20">
          <img src={heroImages[0]} alt="Hero" className="w-full h-full object-cover" />
        </div>
      </section>

      {/* Quick Stats */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-lg text-center">
          <div className="text-3xl font-bold text-blue-600">10K+</div>
          <div className="text-gray-600">Active Taskers</div>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-lg text-center">
          <div className="text-3xl font-bold text-green-600">50K+</div>
          <div className="text-gray-600">Tasks Completed</div>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-lg text-center">
          <div className="text-3xl font-bold text-purple-600">4.9★</div>
          <div className="text-gray-600">Average Rating</div>
        </div>
      </section>

      {/* Service Categories */}
      <section>
        <h2 className="text-3xl font-bold text-center mb-8">Popular Services</h2>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          {serviceCategories.map((category) => (
            <div key={category.id} className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow cursor-pointer">
              <div className={`w-16 h-16 ${category.color} rounded-full flex items-center justify-center text-2xl mx-auto mb-4`}>
                {category.icon}
              </div>
              <h3 className="text-sm font-semibold text-center text-gray-800">{category.name}</h3>
            </div>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section>
        <h2 className="text-3xl font-bold text-center mb-8">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-3xl">📋</span>
            </div>
            <h3 className="text-xl font-semibold mb-2">1. Post Your Task</h3>
            <p className="text-gray-600">Describe what you need done, set your budget, and location</p>
          </div>
          <div className="text-center">
            <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-3xl">🤝</span>
            </div>
            <h3 className="text-xl font-semibold mb-2">2. Get Matched</h3>
            <p className="text-gray-600">Skilled taskers bid on your job with their offers</p>
          </div>
          <div className="text-center">
            <div className="w-20 h-20 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-3xl">✅</span>
            </div>
            <h3 className="text-xl font-semibold mb-2">3. Get It Done</h3>
            <p className="text-gray-600">Track progress, communicate, and pay securely when complete</p>
          </div>
        </div>
      </section>
    </div>
  );
};

// Browse Tasks Page
const BrowseTasksPage = () => {
  const { tasks, user } = useContext(AppContext);
  const [selectedCategory, setSelectedCategory] = useState('all');

  const categories = [
    { id: 'all', name: 'All Tasks' },
    { id: 'delivery', name: 'Delivery' },
    { id: 'cleaning', name: 'Cleaning' },
    { id: 'handyman', name: 'Handyman' },
    { id: 'tutoring', name: 'Tutoring' },
    { id: 'other', name: 'Other' }
  ];

  const filteredTasks = selectedCategory === 'all' 
    ? tasks.filter(task => task.status === 'posted')
    : tasks.filter(task => task.category === selectedCategory && task.status === 'posted');

  const handleAcceptTask = async (taskId) => {
    try {
      await axios.put(`${API}/tasks/${taskId}/accept?tasker_id=${user.id}`);
      alert('Task accepted successfully!');
      // Reload tasks
    } catch (error) {
      console.error('Error accepting task:', error);
      alert('Error accepting task');
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-xl shadow-lg">
        <h2 className="text-2xl font-bold mb-4">Available Tasks</h2>
        
        {/* Category Filter */}
        <div className="flex flex-wrap gap-2 mb-6">
          {categories.map((category) => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                selectedCategory === category.id
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {category.name}
            </button>
          ))}
        </div>

        {/* Tasks List */}
        <div className="space-y-4">
          {filteredTasks.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <p className="text-xl">No tasks available in this category</p>
              <p>Check back later for new opportunities!</p>
            </div>
          ) : (
            filteredTasks.map((task) => (
              <div key={task.id} className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-xl font-semibold">{task.title}</h3>
                    <p className="text-gray-600 capitalize">{task.category.replace('_', ' ')}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-green-600">
                      ${task.budget_min} - ${task.budget_max}
                    </div>
                    <div className="text-sm text-gray-500">
                      {task.priority === 'urgent' && <span className="text-red-500">🔥 Urgent</span>}
                    </div>
                  </div>
                </div>
                
                <p className="text-gray-700 mb-4">{task.description}</p>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4 text-sm text-gray-500">
                    <span>📍 {task.location?.address || 'Location provided after acceptance'}</span>
                    {task.estimated_duration && (
                      <span>⏱️ {task.estimated_duration} mins</span>
                    )}
                  </div>
                  
                  <button
                    onClick={() => handleAcceptTask(task.id)}
                    className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-colors"
                  >
                    Accept Task
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

// Post Task Page
const PostTaskPage = () => {
  const { user, setCurrentView } = useContext(AppContext);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: 'other',
    budget_min: '',
    budget_max: '',
    priority: 'normal',
    estimated_duration: '',
    location: {
      latitude: user?.location?.latitude || 40.7128,
      longitude: user?.location?.longitude || -74.0060,
      address: '',
      is_shared: true
    }
  });

  const categories = [
    { id: 'delivery', name: 'Delivery & Courier' },
    { id: 'cleaning', name: 'Cleaning Services' },
    { id: 'handyman', name: 'Handyman & Repairs' },
    { id: 'moving', name: 'Moving & Lifting' },
    { id: 'beauty', name: 'Beauty & Wellness' },
    { id: 'tech_support', name: 'Tech Support' },
    { id: 'tutoring', name: 'Tutoring & Teaching' },
    { id: 'pet_care', name: 'Pet Care' },
    { id: 'transportation', name: 'Transportation' },
    { id: 'other', name: 'Other Services' }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const taskData = {
        ...formData,
        client_id: user.id,
        budget_min: parseFloat(formData.budget_min),
        budget_max: parseFloat(formData.budget_max),
        estimated_duration: formData.estimated_duration ? parseInt(formData.estimated_duration) : null
      };

      await axios.post(`${API}/tasks`, taskData);
      alert('Task posted successfully!');
      setCurrentView('my-tasks');
    } catch (error) {
      console.error('Error posting task:', error);
      alert('Error posting task');
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white p-8 rounded-xl shadow-lg">
        <h2 className="text-3xl font-bold mb-6">Post a New Task</h2>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Task Title</label>
            <input
              type="text"
              required
              value={formData.title}
              onChange={(e) => setFormData({...formData, title: e.target.value})}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="What do you need help with?"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Category</label>
            <select
              value={formData.category}
              onChange={(e) => setFormData({...formData, category: e.target.value})}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {categories.map((category) => (
                <option key={category.id} value={category.id}>{category.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
            <textarea
              required
              rows={4}
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Provide detailed information about your task..."
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Min Budget ($)</label>
              <input
                type="number"
                required
                min="1"
                value={formData.budget_min}
                onChange={(e) => setFormData({...formData, budget_min: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Max Budget ($)</label>
              <input
                type="number"
                required
                min="1"
                value={formData.budget_max}
                onChange={(e) => setFormData({...formData, budget_max: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
            <input
              type="text"
              value={formData.location.address}
              onChange={(e) => setFormData({
                ...formData, 
                location: {...formData.location, address: e.target.value}
              })}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Enter your address"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Priority</label>
              <select
                value={formData.priority}
                onChange={(e) => setFormData({...formData, priority: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="normal">Normal</option>
                <option value="urgent">Urgent</option>
                <option value="scheduled">Scheduled</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Estimated Duration (minutes)</label>
              <input
                type="number"
                min="15"
                value={formData.estimated_duration}
                onChange={(e) => setFormData({...formData, estimated_duration: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          <button
            type="submit"
            className="w-full bg-blue-500 text-white py-3 rounded-lg font-semibold text-lg hover:bg-blue-600 transition-colors"
          >
            Post Task
          </button>
        </form>
      </div>
    </div>
  );
};

// My Tasks Page
const MyTasksPage = () => {
  const { user, tasks } = useContext(AppContext);
  const [activeTab, setActiveTab] = useState('client');

  const clientTasks = tasks.filter(task => task.client_id === user?.id);
  const taskerTasks = tasks.filter(task => task.tasker_id === user?.id);

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-xl shadow-lg">
        <h2 className="text-2xl font-bold mb-4">My Tasks</h2>
        
        {/* Tabs */}
        <div className="flex space-x-4 mb-6">
          <button
            onClick={() => setActiveTab('client')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'client'
                ? 'bg-blue-500 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            As Client ({clientTasks.length})
          </button>
          <button
            onClick={() => setActiveTab('tasker')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'tasker'
                ? 'bg-blue-500 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            As Tasker ({taskerTasks.length})
          </button>
        </div>

        {/* Tasks List */}
        <div className="space-y-4">
          {(activeTab === 'client' ? clientTasks : taskerTasks).map((task) => (
            <TaskCard key={task.id} task={task} viewMode={activeTab} />
          ))}
          
          {(activeTab === 'client' ? clientTasks : taskerTasks).length === 0 && (
            <div className="text-center py-12 text-gray-500">
              <p className="text-xl">No tasks found</p>
              <p>
                {activeTab === 'client' 
                  ? 'Start by posting your first task!'
                  : 'Browse available tasks to get started!'
                }
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// Task Card Component
const TaskCard = ({ task, viewMode }) => {
  const getStatusColor = (status) => {
    switch(status) {
      case 'posted': return 'bg-blue-100 text-blue-800';
      case 'accepted': return 'bg-yellow-100 text-yellow-800';
      case 'in_progress': return 'bg-purple-100 text-purple-800';
      case 'completed': return 'bg-green-100 text-green-800';
      case 'cancelled': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="border border-gray-200 rounded-lg p-6">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-xl font-semibold">{task.title}</h3>
          <p className="text-gray-600 capitalize">{task.category.replace('_', ' ')}</p>
        </div>
        <div className="text-right">
          <div className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(task.status)}`}>
            {task.status.replace('_', ' ').toUpperCase()}
          </div>
          <div className="text-xl font-bold text-green-600 mt-2">
            ${task.budget_min} - ${task.budget_max}
          </div>
        </div>
      </div>
      
      <p className="text-gray-700 mb-4">{task.description}</p>
      
      <div className="flex items-center justify-between text-sm text-gray-500">
        <span>Created: {new Date(task.created_at).toLocaleDateString()}</span>
        {task.location?.address && (
          <span>📍 {task.location.address}</span>
        )}
      </div>
    </div>
  );
};

// Profile Page
const ProfilePage = () => {
  const { user } = useContext(AppContext);

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="bg-white p-8 rounded-xl shadow-lg">
        <div className="text-center mb-8">
          <div className="w-24 h-24 bg-blue-500 rounded-full flex items-center justify-center text-white text-3xl font-bold mx-auto mb-4">
            {user?.name.charAt(0)}
          </div>
          <h2 className="text-3xl font-bold">{user?.name}</h2>
          <p className="text-gray-600">{user?.email}</p>
          <p className="text-gray-600">{user?.phone}</p>
          <div className="flex items-center justify-center space-x-2 mt-2">
            <span className="text-yellow-500">⭐</span>
            <span className="font-semibold">{user?.rating}</span>
            <span className="text-gray-500">({user?.total_reviews} reviews)</span>
          </div>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Role</label>
            <div className="p-3 bg-gray-50 rounded-lg capitalize">
              {user?.role === 'both' ? 'Client & Tasker' : user?.role}
            </div>
          </div>

          {user?.bio && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Bio</label>
              <div className="p-3 bg-gray-50 rounded-lg">{user.bio}</div>
            </div>
          )}

          {user?.skills && user.skills.length > 0 && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Skills</label>
              <div className="flex flex-wrap gap-2">
                {user.skills.map((skill, index) => (
                  <span key={index} className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Location Sharing</label>
            <div className="p-3 bg-gray-50 rounded-lg">
              {user?.location?.is_shared ? '✅ Enabled' : '❌ Disabled'}
              {user?.location?.address && (
                <div className="text-gray-600 mt-1">📍 {user.location.address}</div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Payments Page
const PaymentsPage = () => {
  const { user } = useContext(AppContext);
  const [activeTab, setActiveTab] = useState('wallet');
  const [walletBalance] = useState(150.50); // Mock data

  const paymentMethods = [
    { id: 1, type: 'card', display: '**** **** **** 1234', name: 'Visa Card' },
    { id: 2, type: 'bank_account', display: '****5678', name: 'Chase Bank' }
  ];

  const transactions = [
    { id: 1, type: 'earned', amount: 75.00, description: 'House cleaning task', date: '2024-01-15' },
    { id: 2, type: 'paid', amount: -25.00, description: 'Delivery service', date: '2024-01-14' },
    { id: 3, type: 'earned', amount: 120.00, description: 'Tech support', date: '2024-01-13' }
  ];

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-xl shadow-lg">
        <h2 className="text-2xl font-bold mb-4">Payments & Wallet</h2>
        
        {/* Tabs */}
        <div className="flex space-x-4 mb-6">
          <button
            onClick={() => setActiveTab('wallet')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'wallet'
                ? 'bg-blue-500 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Neobank Wallet
          </button>
          <button
            onClick={() => setActiveTab('methods')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'methods'
                ? 'bg-blue-500 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Payment Methods
          </button>
          <button
            onClick={() => setActiveTab('history')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'history'
                ? 'bg-blue-500 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Transaction History
          </button>
        </div>

        {/* Wallet Tab */}
        {activeTab === 'wallet' && (
          <div className="space-y-6">
            <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-6 rounded-xl text-white">
              <h3 className="text-lg font-semibold mb-2">TaskMarket Wallet</h3>
              <div className="text-3xl font-bold">${walletBalance.toFixed(2)}</div>
              <p className="text-blue-100 mt-2">Available Balance</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <button className="bg-green-500 text-white p-4 rounded-lg hover:bg-green-600 transition-colors">
                💰 Add Money
              </button>
              <button className="bg-blue-500 text-white p-4 rounded-lg hover:bg-blue-600 transition-colors">
                💸 Withdraw
              </button>
            </div>

            <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-lg">
              <p className="text-sm text-yellow-800">
                <strong>🏦 Neobank Features:</strong> Your TaskMarket wallet acts as a digital bank account with instant transfers, 
                payment splitting, and automatic earnings deposits. Gateway integration coming soon!
              </p>
            </div>
          </div>
        )}

        {/* Payment Methods Tab */}
        {activeTab === 'methods' && (
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="text-lg font-semibold">Linked Payment Methods</h3>
              <button className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors">
                + Add New
              </button>
            </div>

            {paymentMethods.map((method) => (
              <div key={method.id} className="border border-gray-200 p-4 rounded-lg flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
                    {method.type === 'card' ? '💳' : '🏦'}
                  </div>
                  <div>
                    <p className="font-medium">{method.name}</p>
                    <p className="text-sm text-gray-500">{method.display}</p>
                  </div>
                </div>
                <button className="text-red-500 hover:text-red-700">Remove</button>
              </div>
            ))}

            <div className="bg-gray-50 border border-gray-200 p-4 rounded-lg">
              <p className="text-sm text-gray-600">
                <strong>🔒 Secure Integration:</strong> Payment gateway API endpoints are ready for integration. 
                Current placeholder: xxxx-enter-gateway-api-here-xxxx
              </p>
            </div>
          </div>
        )}

        {/* Transaction History Tab */}
        {activeTab === 'history' && (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Recent Transactions</h3>
            
            {transactions.map((transaction) => (
              <div key={transaction.id} className="border border-gray-200 p-4 rounded-lg flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                    transaction.type === 'earned' ? 'bg-green-100' : 'bg-red-100'
                  }`}>
                    {transaction.type === 'earned' ? '💰' : '💸'}
                  </div>
                  <div>
                    <p className="font-medium">{transaction.description}</p>
                    <p className="text-sm text-gray-500">{transaction.date}</p>
                  </div>
                </div>
                <div className={`text-lg font-semibold ${
                  transaction.type === 'earned' ? 'text-green-600' : 'text-red-600'
                }`}>
                  {transaction.type === 'earned' ? '+' : ''}${Math.abs(transaction.amount).toFixed(2)}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

// Bottom Navigation
const BottomNavigation = () => {
  const { currentView, setCurrentView } = useContext(AppContext);

  const navItems = [
    { id: 'home', label: 'Home', icon: '🏠' },
    { id: 'browse-tasks', label: 'Browse', icon: '🔍' },
    { id: 'post-task', label: 'Post', icon: '➕' },
    { id: 'my-tasks', label: 'My Tasks', icon: '📋' },
    { id: 'profile', label: 'Profile', icon: '👤' }
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-4 py-2">
      <div className="container mx-auto">
        <div className="flex justify-around">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setCurrentView(item.id)}
              className={`flex flex-col items-center py-2 px-3 rounded-lg transition-colors ${
                currentView === item.id
                  ? 'bg-blue-100 text-blue-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              <span className="text-xl mb-1">{item.icon}</span>
              <span className="text-xs font-medium">{item.label}</span>
            </button>
          ))}
        </div>
      </div>
    </nav>
  );
};

export default App;