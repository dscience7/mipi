## Introduction
Python package for gathering data from the UK National Grid gas transmission Market Information Provision Initiative (MIPI) API. 

## Installation
1. Clone repository
2. Create python environment using requirements.txt

## Usage

```
from mipi import Mipi
import datetime as dt
M = Mipi()
start = dt.date(2020, 1, 1) end = dt.date(2020, 4, 1)
demand = M.get_physical_flows(from_date=start, to_date=end)
```


