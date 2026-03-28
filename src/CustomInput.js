import React from "react";

function CustomInput({ type, name, placeholder, value, onChange }) {
  return (
    <div style={{ margin: "10px 0" }}>
      <input
        type={type}
        name={name}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        style={{ width: "100%", padding: "8px" }}
      />
    </div>
  );
}

export default CustomInput;