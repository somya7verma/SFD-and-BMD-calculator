# SFD and BMD Calculator 📐

A **Python desktop application** that generates **Shear Force Diagrams (SFD)** and **Bending Moment Diagrams (BMD)** for a cantilever beam subjected to multiple Uniformly Distributed Loads (UDLs) at different positions along the beam length.

Built with **Tkinter** for the GUI and **Matplotlib** for interactive diagram plotting.

---

## 🧩 Problem Statement

> To develop a generalised computer program for the generation of support reactions, SFD and BMD of a **cantilever beam** subjected to different UDLs at different locations over the length of the beam.

---

## ✨ Features

- 🏗️ **Cantilever Beam Analysis** — Computes support reactions (force & moment) at the fixed end
- 📊 **Shear Force Diagram (SFD)** — Plots shear force variation along the beam length
- 📈 **Bending Moment Diagram (BMD)** — Plots bending moment variation along the beam length
- ➕ **Multiple UDL Support** — Add up to **4 UDL segments** at different positions
- 🖱️ **Interactive Hover** — Hover over plots to see exact `(x, shear/moment)` values
- 🪟 **Clean GUI** — Built with Tkinter; results open in a maximised results window

---

## 🖼️ UI Overview

| Input Field | Description |
|---|---|
| Beam Length | Total length of the cantilever beam (in metres) |
| Start Point | Starting position of the UDL on the beam (m) |
| End Point | Ending position of the UDL on the beam (m) |
| Magnitude | Intensity of the UDL (N/m) |

> Default units: Length → **m**, Load → **N/m**, Reaction Force → **N**, Moment → **Nm**

---

## 🚀 Getting Started

### Prerequisites

Make sure you have **Python 3.x** installed, then install the required libraries:

```bash
pip install numpy matplotlib
```

> `tkinter` is included with the standard Python installation on Windows.

### Running the Application

```bash
python sfd_bmd_calculator.py
```

---

## 🛠️ How to Use

1. **Enter the beam length** in the input field at the top.
2. **Enter the first UDL** — provide the start point, end point, and magnitude.
3. Click **"Add More"** to add additional UDL segments (up to 4 total).
4. Click **"Calculate"** to generate the SFD and BMD plots.
5. **Hover over** any point on the diagram to view exact values.
6. Click **"Exit"** to close the application.

---

## 📁 Project Structure

```
SFD-and-BMD-calculator/
│
├── sfd_bmd_calculator.py   # Main application file
└── README.md               # Project documentation
```

---

## 📐 Calculation Methodology

1. **UDL → Point Load Conversion**: Each UDL is converted to an equivalent point load acting at the centroid of the loaded region.
2. **Reaction Calculation**:
   - `Reaction Force (R) = Σ (w × L_segment)`
   - `Reaction Moment (M) = -Σ (w × L_segment × x_centroid)`
3. **SFD**: Shear force at any section `x` is computed by summing all load effects to the right of the section.
4. **BMD**: Bending moment at any section `x` is computed by summing moment contributions from all loads to the right of section `x`.

---

## 🔧 Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.x | Core language |
| Tkinter | GUI framework |
| Matplotlib | Plotting SFD & BMD |
| NumPy | Numerical computation |

---

## 👩‍💻 Author

**Somya Verma**  
1st Year Engineering Student  
GitHub: [@somya7verma](https://github.com/somya7verma)

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
