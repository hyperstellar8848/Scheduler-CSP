Model and solve a university course scheduling problem using **Constraint Satisfaction Problems (CSP)**.

Implement and compare:
- Backtracking Search
- Min-Conflicts Local Search

---

# Problem Description

Schedule university classes by assigning a **day**, **time slot**, and **room** while satisfying all required constraints.

---

# Variables

Each class is a variable.

Example:

- C1
- C2
- C3
- ...

Each class has:
- Professor
- Student Group
- Type (Theory / Lab)

---

# Domains

### Days
- Saturday
- Sunday
- Monday
- Tuesday
- Wednesday

### Time Slots
- 08:00–10:00
- 10:00–12:00
- 14:00–16:00
- 16:00–18:00

### Rooms
- A101
- A102
- B201
- B202

---

# Constraints

## Hard Constraints

- Every class must have exactly one day, time, and room.
- A professor cannot teach two classes at the same time.
- A room cannot host two classes simultaneously.
- Lab classes must be scheduled only in:
  - B201
  - B202

---

## Soft Constraints

- Professor **X** prefers morning classes.
- Student groups prefer classes not to be scheduled consecutively.

---

# Implementation

## 1. CSP Modeling

Represent:

- Variables
- Domains
- Constraints

using Python dictionaries or JSON.

---

## 2. Backtracking Search

Implement:

- MRV (Minimum Remaining Values)
- LCV (Least Constraining Value)
- Forward Checking

---

## 3. Min-Conflicts Search

Implement:

- Random initial assignment
- Select variable with the most conflicts
- Assign a value that minimizes conflicts
- Repeat until a solution is found or iteration limit is reached

---

# Input

Example JSON:

```json
{
  "classes": [
    {
      "id": "C1",
      "professor": "Dr. A",
      "type": "Theory",
      "group": "G1"
    },
    {
      "id": "C2",
      "professor": "Dr. B",
      "type": "Lab",
      "group": "G2"
    },
    {
      "id": "C3",
      "professor": "Dr. C",
      "type": "Theory",
      "group": "G1"
    }
  ],

  "days": [
    "Saturday",
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday"
  ],

  "time_slots": [
    "8-10",
    "10-12",
    "14-16",
    "16-18"
  ],

  "rooms": [
    "A101",
    "A102",
    "B201",
    "B202"
  ]
}
```

---

# Output

Generate a valid schedule showing:

- Class
- Day
- Time Slot
- Room

while satisfying all hard constraints and minimizing soft constraint violations.
