// var
var greeting = "Good Morning!";
console.log(greeting);

// let
let name = "Alice";
console.log(name);

// const
const pi = 3.14159;
console.log(pi);


// Regular function
function add(a, b) {
    return a + b;
}
console.log("add(5, 3):", add(5, 3));

// Arrow function
const multiply = (a, b) => a * b;
console.log("multiply(4, 6):", multiply(4, 6));


const person = {
    firstName: "Dibash",
    lastName: "Bade",
    age: 20,
    greet() {
        return `Hi, I'm ${this.firstName} ${this.lastName}`;
    }
};

//ARRAYS
const numbers = [1, 2, 3, 4, 5];

// map: create a new array with each number doubled
const doubled = numbers.map(num => num * 2);
console.log("Doubled:", doubled);

// filter: create a new array with numbers greater than 3
const filtered = numbers.filter(num => num > 3);
console.log("Filtered (>3):", filtered);

//SPREAD OPERATOR

//Copying an array
const newNumbers = [...numbers, 6, 7];
console.log("New Numbers:", newNumbers);