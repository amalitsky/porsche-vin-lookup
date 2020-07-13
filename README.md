# Porsche VIN lookup
Porsche VIN lookup (assemble date, price, options) python script.
Experimenting with Python for the sake of it.
Uses [vinanalytics.com website](https://vinanalytics.com) under the hood.

## Usage
Run `user@i386:src$ python3 lookup.py WP0CB2A89HS241174` command.
Where _WP0CB2A89HS241174_ is VIN number of Porsche vehicle.
Some valid VINs are not present in DB and that is somewhat expected.

### Report example:
```
WP0CB2A89HS241174
718 Boxster S
2016-12-01
GT Silver Metallic
Leather Interior in Black
$97,480.00

220: Porsche Torque Vectoring (PTV)
475: Porsche Active Suspension Management (PASM)
QR5: Sport Chrono Package
...

25081: Seat Stitching in Deviated Thread
446: Wheel center caps with colored Porsche Crest
546: Supplemental Safety Bars in Exterior Color
...
```

### Output format
There are three sections:
- basic info about the car: VIN, assembly date, etc
- car options I deemed important/desired (bold font)
- rest of options.

Options are _loosely_ ordered by option code number.

### Python dependencies
- python3
- beautiful soap v4
- requests library
