# Optimization Methods

This repository contains Python implementations of optimization techniques used to solve Linear Programming and Transportation Problems.

## Programs

### 1. Big-M Simplex Method

**File:** `big_m.py`

The program solves a Linear Programming Problem (LPP) using the Big-M Simplex Method.

It handles constraints involving:
- Slack variables
- Surplus variables
- Artificial variables

The program determines:
- Optimal values of the decision variables
- Maximum objective-function value

### 2. Transportation Problem

**File:** `vam_modi.py`

This program implements two methods for solving a Transportation Problem:

#### Vogel's Approximation Method (VAM)

VAM is used to obtain an Initial Basic Feasible Solution (IBFS) by calculating penalties and making allocations based on the transportation costs.

#### MODI Method

The MODI (Modified Distribution) Method is used to test the transportation solution for optimality and improve the allocation when a lower transportation cost is possible.

The program determines:
- Shipment allocation
- Optimal transportation plan
- Minimum total transportation cost

## Requirements

- Python 3.x
- NumPy

Install NumPy using:

```bash
pip install numpy
