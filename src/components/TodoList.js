import React from "react";
import TodoItem from "./TodoItem";

function TodoList({ todos, deleteTodo, editTodo }) {
  return (
    <div className="todo-list">
      {todos.length === 0 ? (
        <p>No todos yet!</p>
      ) : (
        todos.map((todo) => (
          <TodoItem
            key={todo.id}
            todo={todo}
            deleteTodo={deleteTodo}
            editTodo={editTodo}
          />
        ))
      )}
    </div>
  );
}

export default TodoList;