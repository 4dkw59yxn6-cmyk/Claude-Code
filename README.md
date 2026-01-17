# Massachusetts SMART Solar Incentive Calculator

A Python script to calculate Massachusetts Solar Massachusetts Renewable Target (SMART) program incentive rates and projected revenue for solar installations.

## Overview

The SMART program is Massachusetts' solar incentive program that provides per-kWh incentive payments for solar energy generation over a 10-year period. This calculator helps estimate:

- Total incentive rate ($/kWh) based on system size and applicable adders
- Annual revenue projections
- 10-year total revenue

## Features

- **Base Rate Calculation**: Automatically determines the correct base compensation rate based on system size tiers
- **Adder Support**: Includes common SMART adders:
  - Low-Income / Community Shared Solar
  - Energy Storage Systems
  - Location-Based (landfill, brownfield, carport)
  - Pollinator-Friendly Habitat
- **Revenue Projections**: Calculates annual and 10-year revenue based on estimated production
- **Multiple Examples**: Includes pre-configured examples for different system types

## Requirements

- Python 3.6 or higher
- No external dependencies required (uses only Python standard library)

## Installation

1. Clone this repository or download `smart_calculator.py`
2. No additional installation required

## Usage

### Running the Examples

Run the script directly to see four pre-configured examples:

```bash
python3 smart_calculator.py
```

This will show calculations for:
1. Small residential system (10 kW)
2. Low-income residential system (20 kW)
3. Commercial system with storage (500 kW)
4. Large ground-mount system (2,000 kW)

### Using as a Python Module

Import and use the calculator in your own Python code:

```python
from smart_calculator import SMARTCalculator

# Initialize calculator
calculator = SMARTCalculator(program_year='py2025')

# Calculate for a 100 kW system with energy storage
results = calculator.calculate(
    system_size_kw=100,
    adders=['energy_storage'],
    annual_production_kwh_per_kw=1200  # Optional, defaults to 1200
)

# Print formatted results
calculator.print_results(results)

# Or access individual values
print(f"Total Rate: ${results['total_rate']:.4f}/kWh")
print(f"10-Year Revenue: ${results['total_revenue']:,.2f}")
```

### Available Adders

To see all available adders:

```python
from smart_calculator import SMARTCalculator

SMARTCalculator.list_available_adders()
```

Current adders include:
- `low_income` - Low-Income or Community Shared Solar
- `energy_storage` - Energy Storage System (2+ hours, 25% capacity)
- `location_based` - Preferred location (landfill, brownfield, carport)
- `pollinator_habitat` - Pollinator-friendly habitat

### Custom Calculations

```python
from smart_calculator import SMARTCalculator

calculator = SMARTCalculator(program_year='py2025')

# Example: 250 kW carport system with energy storage
results = calculator.calculate(
    system_size_kw=250,
    adders=['location_based', 'energy_storage'],
    annual_production_kwh_per_kw=1300  # Higher production assumption
)

calculator.print_results(results)
```

## Program Year Support

Currently supports:
- **PY2025**: Program Year 2025 rates (default)

To update for future program years, add new rate tiers to the `BASE_RATES` dictionary in the `SMARTCalculator` class.

## Understanding the Output

The calculator provides:

### Incentive Rates Section
- **Base Rate**: The base compensation rate for your system size tier
- **Applied Adders**: Additional incentive rates for qualifying characteristics
- **Total Incentive Rate**: Sum of base rate and all adders

### Revenue Projection Section
- **Annual Production**: Estimated kWh generated per year (based on system size × production factor)
- **Annual Revenue**: Yearly incentive payment (production × total rate)
- **Total 10-Year Revenue**: Total incentive payments over the 10-year term

## Important Notes

1. **Rates are Approximate**: This calculator uses Program Year 2025 rates as a reference. Actual rates vary by:
   - Program year
   - Utility territory
   - Specific project characteristics
   - Available capacity

2. **Production Estimates**: Default production assumes 1,200 kWh/kW/year. Actual production varies by:
   - Location and solar resource
   - System design and orientation
   - Shading and other site conditions

3. **Adder Eligibility**: Not all adders are available for all projects. Requirements include:
   - Low-Income: Must serve qualified low-income or affordable housing
   - Energy Storage: Required for certain large ground-mount systems
   - Location-Based: Must be on approved site types
   - Pollinator Habitat: Must meet habitat certification requirements

4. **Official Rates**: Always consult official SMART program documentation for:
   - Current program year rates
   - Eligibility requirements
   - Application procedures

## References

- [SMART 3.0 Program Details](https://www.mass.gov/info-details/smart-30-program-details)
- [Program Year 2026 Report](https://www.mass.gov/doc/draft-program-year-2026-annual-report)
- [SMART Program Overview](https://www.mass.gov/solar-massachusetts-renewable-target-smart-program)

## System Size Tiers (PY2025)

| System Size (kW AC) | Base Rate ($/kWh) |
|---------------------|-------------------|
| 0 - 25             | 0.0300           |
| 25 - 250           | 0.2482           |
| 250 - 500          | 0.2482           |
| 500 - 1,000        | 0.2113           |
| 1,000 - 5,000      | 0.1729           |
| > 5,000            | 0.1729           |

## Example Output

```
============================================================
MASSACHUSETTS SMART SOLAR INCENTIVE CALCULATOR
============================================================

Program Year: PY2025
System Size: 500.0 kW AC

------------------------------------------------------------
INCENTIVE RATES
------------------------------------------------------------
Base Rate: $0.2482/kWh

Applied Adders:
  • Energy Storage System (2+ hours, 25% capacity): $0.0200/kWh
  • Preferred location (landfill, brownfield, carport): $0.0600/kWh

Total Adder Value: $0.0800/kWh

============================================================
TOTAL INCENTIVE RATE: $0.3282/kWh
============================================================

------------------------------------------------------------
REVENUE PROJECTION (10-YEAR)
------------------------------------------------------------
Annual Production: 600,000 kWh/year
Annual Revenue: $196,920.00/year
Incentive Period: 10 years

============================================================
TOTAL 10-YEAR REVENUE: $1,969,200.00
============================================================
```

## Contributing

To update rates for new program years:

1. Add new rates to `BASE_RATES` dictionary
2. Update adder values in `ADDERS` dictionary if changed
3. Update documentation and examples

## License

This is a reference implementation. Consult official SMART program documentation for authoritative information.

## Disclaimer

This calculator is for estimation purposes only. Actual incentive rates and revenue will vary based on official program rules, utility territory, capacity availability, and other factors. Always consult with the Massachusetts Department of Energy Resources (DOER) and your utility for official rates and eligibility requirements.
