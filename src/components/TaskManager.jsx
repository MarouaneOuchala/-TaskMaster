import React, { useState } from 'react';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import { FiSun, FiMoon, FiMenu } from 'react-icons/fi';
import '../styles/TaskManager.css';

const TaskManager = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [tasks, setTasks] = useState([
    {
      id: '1',
      title: 'Complete project proposal',
      category: 'Work',
      priority: 'high',
      dueDate: '2024-04-10',
      completed: false,
    },
    {
      id: '2',
      title: 'Buy groceries',
      category: 'Shopping',
      priority: 'medium',
      dueDate: '2024-04-05',
      completed: true,
    },
    // Add more sample tasks here
  ]);

  const categories = [
    { id: 'all', name: 'All Tasks', count: tasks.length },
    { id: 'work', name: 'Work', count: tasks.filter(t => t.category === 'Work').length },
    { id: 'shopping', name: 'Shopping', count: tasks.filter(t => t.category === 'Shopping').length },
  ];

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    document.documentElement.classList.toggle('dark');
  };

  const onDragEnd = (result) => {
    if (!result.destination) return;

    const items = Array.from(tasks);
    const [reorderedItem] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reorderedItem);

    setTasks(items);
  };

  const completedTasksCount = tasks.filter(task => task.completed).length;
  const progress = (completedTasksCount / tasks.length) * 100;

  return (
    <div className={`min-h-screen dark-mode-transition ${darkMode ? 'dark' : ''}`}>
      <div className="flex h-screen bg-gray-100 dark:bg-gray-900">
        {/* Sidebar */}
        <div className={`
          sidebar-transition fixed inset-y-0 left-0 z-30 w-64 transform
          ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
          bg-white dark:bg-gray-800 shadow-lg md:relative md:translate-x-0
        `}>
          <div className="flex items-center justify-between p-4 border-b dark:border-gray-700">
            <h1 className="text-xl font-bold text-gray-800 dark:text-white">Task Manager</h1>
            <button
              onClick={() => setSidebarOpen(false)}
              className="md:hidden text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
            >
              <FiMenu size={24} />
            </button>
          </div>

          <div className="p-4">
            <div className="progress-bar">
              <div
                className="progress-bar-fill"
                style={{ width: `${progress}%` }}
              />
            </div>
            <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
              {completedTasksCount} of {tasks.length} tasks completed
            </p>
          </div>

          <nav className="mt-4 px-4">
            {categories.map((category) => (
              <a
                key={category.id}
                href="#"
                className="flex items-center justify-between px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors duration-200"
              >
                <span>{category.name}</span>
                <span className="category-badge bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-300 px-2 py-1 rounded-full text-xs">
                  {category.count}
                </span>
              </a>
            ))}
          </nav>
        </div>

        {/* Main Content */}
        <div className="flex-1 overflow-auto">
          <header className="bg-white dark:bg-gray-800 shadow-sm">
            <div className="flex items-center justify-between px-6 py-4">
              <button
                onClick={() => setSidebarOpen(true)}
                className="md:hidden text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
              >
                <FiMenu size={24} />
              </button>
              <div className="flex items-center space-x-4">
                <button
                  onClick={toggleDarkMode}
                  className="dark-mode-toggle p-2 text-gray-700 dark:text-gray-300"
                >
                  {darkMode ? <FiSun size={20} /> : <FiMoon size={20} />}
                </button>
              </div>
            </div>
          </header>

          <main className="p-6">
            <DragDropContext onDragEnd={onDragEnd}>
              <Droppable droppableId="tasks">
                {(provided) => (
                  <div
                    {...provided.droppableProps}
                    ref={provided.innerRef}
                    className="space-y-4 task-list"
                  >
                    {tasks.map((task, index) => (
                      <Draggable key={task.id} draggableId={task.id} index={index}>
                        {(provided) => (
                          <div
                            ref={provided.innerRef}
                            {...provided.draggableProps}
                            {...provided.dragHandleProps}
                            className="task-card bg-white dark:bg-gray-800 rounded-lg shadow-sm hover:shadow-md p-4"
                          >
                            <div className="flex items-center justify-between">
                              <div className="flex items-center space-x-3">
                                <input
                                  type="checkbox"
                                  checked={task.completed}
                                  onChange={() => {
                                    const updatedTasks = [...tasks];
                                    updatedTasks[index].completed = !updatedTasks[index].completed;
                                    setTasks(updatedTasks);
                                  }}
                                  className="custom-checkbox"
                                />
                                <span className={`text-gray-800 dark:text-gray-200 ${task.completed ? 'line-through text-gray-500' : ''}`}>
                                  {task.title}
                                </span>
                              </div>
                              <div className="flex items-center space-x-2">
                                <span className={`
                                  px-2 py-1 text-xs font-medium rounded-full text-white
                                  priority-${task.priority}
                                `}>
                                  {task.priority}
                                </span>
                                <span className="text-sm text-gray-500 dark:text-gray-400">
                                  {task.dueDate}
                                </span>
                              </div>
                            </div>
                          </div>
                        )}
                      </Draggable>
                    ))}
                    {provided.placeholder}
                  </div>
                )}
              </Droppable>
            </DragDropContext>
          </main>
        </div>
      </div>
    </div>
  );
};

export default TaskManager; 