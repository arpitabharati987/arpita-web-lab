import React, { useState } from "react";
import TodoList from "./components/TodoList";

function App() {
  const [todos, setTodos] = useState([]);
  const [input, setInput] = useState("");

  // Add Todo
  const addTodo = () => {
    if (input.trim() === "") return;
    setTodos([...todos, { id: Date.now(), text: input }]);
    setInput("");
  };

  // Delete Todo
  const deleteTodo = (id) => {
    setTodos(todos.filter((todo) => todo.id !== id));
  };

  // Edit Todo
  const editTodo = (id, newText) => {
    setTodos(
      todos.map((todo) => (todo.id === id ? { ...todo, text: newText } : todo))
    );
  };

  return (
    <div className="app">
      <h1>My Todo App</h1>
      <div className="input-section">
        <input
          type="text"
          placeholder="Add a todo..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button onClick={addTodo}>Add</button>
      </div>
      <TodoList todos={todos} deleteTodo={deleteTodo} editTodo={editTodo} />
    </div>
  );
}

export default App;