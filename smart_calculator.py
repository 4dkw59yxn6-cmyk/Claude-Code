#!/usr/bin/env python3
"""
Massachusetts SMART Solar Incentive Calculator

This script calculates the total incentive rate and projected 10-year revenue
for solar installations under the Massachusetts SMART 3.0 program.

Based on Program Year 2025 rates (update annually as new rates are published).
"""

import csv
from datetime import datetime
from typing import Dict, List


class SMARTCalculator:
    """Calculator for Massachusetts SMART solar incentive rates."""

    # Program Year 2025 Base Compensation Rates ($/kWh)
    # Rates are based on system size tiers
    BASE_RATES = {
        'py2025': {
            (0, 25): 0.03,        # Small systems ≤25 kW (flat rate)
            (25, 250): 0.2482,    # 25-250 kWac
            (250, 500): 0.2482,   # 250-500 kWac
            (500, 1000): 0.2113,  # 500-1,000 kWac
            (1000, 5000): 0.1729, # 1,000-5,000 kWac
            (5000, float('inf')): 0.1729  # >5,000 kWac
        }
    }

    # Available Adders ($/kWh)
    ADDERS = {
        'low_income': {
            'description': 'Low-Income or Community Shared Solar',
            'rate': 0.06,  # For systems ≤25 kW (doubles base rate to $0.06)
            'rate_large': 0.03  # Approximate adder for larger systems
        },
        'energy_storage': {
            'description': 'Energy Storage System (2+ hours, 25% capacity)',
            'rate': 0.02  # Approximate adder
        },
        'location_based': {
            'description': 'Preferred location (landfill, brownfield, carport)',
            'rate': 0.06  # Approximate adder
        },
        'pollinator_habitat': {
            'description': 'Pollinator-friendly habitat',
            'rate': 0.01  # Approximate adder
        }
    }

    def __init__(self, program_year: str = 'py2025'):
        """
        Initialize the calculator.

        Args:
            program_year: Program year for rate lookup (e.g., 'py2025', 'py2026')
        """
        self.program_year = program_year
        if program_year not in self.BASE_RATES:
            raise ValueError(f"Program year {program_year} not available. "
                           f"Available: {list(self.BASE_RATES.keys())}")

    def get_base_rate(self, system_size_kw: float) -> float:
        """
        Get the base compensation rate for a given system size.

        Args:
            system_size_kw: System size in kW AC

        Returns:
            Base compensation rate in $/kWh
        """
        rates = self.BASE_RATES[self.program_year]
        for (min_size, max_size), rate in rates.items():
            if min_size < system_size_kw <= max_size:
                return rate
        return 0.0

    def calculate_total_rate(
        self,
        system_size_kw: float,
        adders: List[str]
    ) -> Dict:
        """
        Calculate the total incentive rate including adders.

        Args:
            system_size_kw: System size in kW AC
            adders: List of adder names to apply (e.g., ['low_income', 'energy_storage'])

        Returns:
            Dictionary containing base rate, adder details, and total rate
        """
        base_rate = self.get_base_rate(system_size_kw)

        applied_adders = []
        total_adder_value = 0.0

        for adder_name in adders:
            if adder_name not in self.ADDERS:
                print(f"Warning: Unknown adder '{adder_name}' - skipping")
                continue

            adder_info = self.ADDERS[adder_name]

            # Special handling for low-income adder based on system size
            if adder_name == 'low_income':
                if system_size_kw <= 25:
                    adder_rate = adder_info['rate'] - base_rate  # Doubles to $0.06
                else:
                    adder_rate = adder_info['rate_large']
            else:
                adder_rate = adder_info['rate']

            applied_adders.append({
                'name': adder_name,
                'description': adder_info['description'],
                'rate': adder_rate
            })
            total_adder_value += adder_rate

        total_rate = base_rate + total_adder_value

        return {
            'base_rate': base_rate,
            'adders': applied_adders,
            'total_adder_value': total_adder_value,
            'total_rate': total_rate
        }

    def calculate_revenue(
        self,
        system_size_kw: float,
        total_rate: float,
        annual_production_kwh_per_kw: float = 1200,
        incentive_period_years: int = 10
    ) -> Dict:
        """
        Calculate projected revenue over the incentive period.

        Args:
            system_size_kw: System size in kW AC
            total_rate: Total incentive rate in $/kWh
            annual_production_kwh_per_kw: Annual production per kW (default: 1200 kWh/kW)
            incentive_period_years: Incentive period in years (default: 10)

        Returns:
            Dictionary containing revenue projections
        """
        annual_production_kwh = system_size_kw * annual_production_kwh_per_kw
        annual_revenue = annual_production_kwh * total_rate
        total_revenue = annual_revenue * incentive_period_years

        return {
            'annual_production_kwh': annual_production_kwh,
            'annual_revenue': annual_revenue,
            'incentive_period_years': incentive_period_years,
            'total_revenue': total_revenue
        }

    def calculate(
        self,
        system_size_kw: float,
        adders: List[str] = None,
        annual_production_kwh_per_kw: float = 1200,
        incentive_period_years: int = 10
    ) -> Dict:
        """
        Complete calculation of incentive rate and revenue.

        Args:
            system_size_kw: System size in kW AC
            adders: List of adder names to apply
            annual_production_kwh_per_kw: Annual production per kW (default: 1200 kWh/kW)
            incentive_period_years: Incentive period in years (default: 10, can be 20)

        Returns:
            Dictionary containing all calculation results
        """
        if adders is None:
            adders = []

        rate_info = self.calculate_total_rate(system_size_kw, adders)
        revenue_info = self.calculate_revenue(
            system_size_kw,
            rate_info['total_rate'],
            annual_production_kwh_per_kw,
            incentive_period_years
        )

        return {
            'system_size_kw': system_size_kw,
            'program_year': self.program_year,
            **rate_info,
            **revenue_info
        }

    @staticmethod
    def print_results(results: Dict):
        """
        Print calculation results in a formatted manner.

        Args:
            results: Results dictionary from calculate()
        """
        print("\n" + "="*60)
        print("MASSACHUSETTS SMART SOLAR INCENTIVE CALCULATOR")
        print("="*60)
        print(f"\nProgram Year: {results['program_year'].upper()}")
        print(f"System Size: {results['system_size_kw']:,.1f} kW AC")
        print(f"\n{'-'*60}")
        print("INCENTIVE RATES")
        print(f"{'-'*60}")
        print(f"Base Rate: ${results['base_rate']:.4f}/kWh")

        if results['adders']:
            print(f"\nApplied Adders:")
            for adder in results['adders']:
                print(f"  • {adder['description']}: ${adder['rate']:.4f}/kWh")
            print(f"\nTotal Adder Value: ${results['total_adder_value']:.4f}/kWh")

        print(f"\n{'='*60}")
        print(f"TOTAL INCENTIVE RATE: ${results['total_rate']:.4f}/kWh")
        print(f"{'='*60}")

        years = results['incentive_period_years']
        print(f"\n{'-'*60}")
        print(f"REVENUE PROJECTION ({years}-YEAR)")
        print(f"{'-'*60}")
        print(f"Annual Production: {results['annual_production_kwh']:,.0f} kWh/year")
        print(f"Annual Revenue: ${results['annual_revenue']:,.2f}/year")
        print(f"Incentive Period: {years} years")
        print(f"\n{'='*60}")
        print(f"TOTAL {years}-YEAR REVENUE: ${results['total_revenue']:,.2f}")
        print(f"{'='*60}\n")

    @staticmethod
    def list_available_adders():
        """Print all available adders and their descriptions."""
        print("\n" + "="*60)
        print("AVAILABLE ADDERS")
        print("="*60)
        for name, info in SMARTCalculator.ADDERS.items():
            rate = info.get('rate', info.get('rate_large', 0))
            print(f"\n{name}:")
            print(f"  Description: {info['description']}")
            print(f"  Rate: ~${rate:.4f}/kWh")
        print("\n" + "="*60 + "\n")

    @staticmethod
    def export_to_csv(results: Dict, filename: str = None, scenario_name: str = "Scenario"):
        """
        Export a single calculation result to CSV file for Google Sheets import.

        Args:
            results: Results dictionary from calculate()
            filename: Output filename (default: smart_calculation_YYYYMMDD_HHMMSS.csv)
            scenario_name: Name for this scenario (default: "Scenario")

        Returns:
            The filename that was created
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"smart_calculation_{timestamp}.csv"

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Header
            writer.writerow(['Massachusetts SMART Solar Incentive Calculator'])
            writer.writerow([f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
            writer.writerow([])

            # Scenario info
            writer.writerow(['Scenario', scenario_name])
            writer.writerow(['Program Year', results['program_year'].upper()])
            writer.writerow(['System Size (kW AC)', results['system_size_kw']])
            writer.writerow([])

            # Rates
            writer.writerow(['INCENTIVE RATES'])
            writer.writerow(['Base Rate ($/kWh)', f"{results['base_rate']:.4f}"])

            if results['adders']:
                writer.writerow([])
                writer.writerow(['Applied Adders', 'Rate ($/kWh)'])
                for adder in results['adders']:
                    writer.writerow([adder['description'], f"{adder['rate']:.4f}"])
                writer.writerow(['Total Adder Value', f"{results['total_adder_value']:.4f}"])

            writer.writerow([])
            writer.writerow(['TOTAL INCENTIVE RATE ($/kWh)', f"{results['total_rate']:.4f}"])
            writer.writerow([])

            # Revenue
            writer.writerow(['REVENUE PROJECTION'])
            writer.writerow(['Annual Production (kWh/year)', f"{results['annual_production_kwh']:.0f}"])
            writer.writerow(['Annual Revenue ($/year)', f"{results['annual_revenue']:.2f}"])
            writer.writerow(['Incentive Period (years)', results['incentive_period_years']])
            writer.writerow([f"TOTAL {results['incentive_period_years']}-YEAR REVENUE ($)", f"{results['total_revenue']:.2f}"])

        print(f"\n✓ Exported to: {filename}")
        return filename

    @staticmethod
    def export_batch_to_csv(results_list: List[Dict], filename: str = None):
        """
        Export multiple calculation results to CSV file for Google Sheets import.
        Creates a comparison table format.

        Args:
            results_list: List of results dictionaries from calculate()
            filename: Output filename (default: smart_batch_YYYYMMDD_HHMMSS.csv)

        Returns:
            The filename that was created
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"smart_batch_{timestamp}.csv"

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Header
            writer.writerow(['Massachusetts SMART Solar Incentive Calculator - Batch Comparison'])
            writer.writerow([f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
            writer.writerow([])

            # Column headers
            num_scenarios = len(results_list)
            headers = ['Parameter'] + [f'Scenario {i+1}' for i in range(num_scenarios)]
            writer.writerow(headers)

            # System info
            writer.writerow(['System Size (kW AC)'] + [r['system_size_kw'] for r in results_list])
            writer.writerow(['Program Year'] + [r['program_year'].upper() for r in results_list])

            # Adders applied
            max_adders = max(len(r['adders']) for r in results_list)
            if max_adders > 0:
                writer.writerow([])
                writer.writerow(['Applied Adders'] + [''] * num_scenarios)
                for i in range(max_adders):
                    row = [f'  Adder {i+1}']
                    for r in results_list:
                        if i < len(r['adders']):
                            row.append(r['adders'][i]['description'])
                        else:
                            row.append('')
                    writer.writerow(row)

            writer.writerow([])
            writer.writerow(['RATES'])
            writer.writerow(['Base Rate ($/kWh)'] + [f"{r['base_rate']:.4f}" for r in results_list])
            writer.writerow(['Total Adder Value ($/kWh)'] + [f"{r['total_adder_value']:.4f}" for r in results_list])
            writer.writerow(['TOTAL RATE ($/kWh)'] + [f"{r['total_rate']:.4f}" for r in results_list])

            writer.writerow([])
            writer.writerow(['REVENUE PROJECTIONS'])
            writer.writerow(['Annual Production (kWh)'] + [f"{r['annual_production_kwh']:.0f}" for r in results_list])
            writer.writerow(['Annual Revenue ($)'] + [f"{r['annual_revenue']:.2f}" for r in results_list])
            writer.writerow(['Incentive Period (years)'] + [r['incentive_period_years'] for r in results_list])
            writer.writerow(['TOTAL REVENUE ($)'] + [f"{r['total_revenue']:.2f}" for r in results_list])

            # ROI comparison (if we had system costs)
            writer.writerow([])
            writer.writerow(['Note: Import this CSV into Google Sheets for easy analysis and charting'])

        print(f"\n✓ Exported batch comparison to: {filename}")
        print(f"  Contains {num_scenarios} scenario(s)")
        return filename


def main():
    """Main function demonstrating calculator usage."""
    calculator = SMARTCalculator(program_year='py2025')

    print("\n" + "="*60)
    print("Massachusetts SMART Solar Incentive Calculator")
    print("="*60)
    print("\nThis calculator estimates SMART incentive rates and revenue")
    print("based on Program Year 2025 rates.\n")

    # Example 1: Small residential system (10 kW) with no adders
    print("\n### EXAMPLE 1: Small Residential System ###")
    results1 = calculator.calculate(
        system_size_kw=10,
        adders=[]
    )
    calculator.print_results(results1)

    # Example 2: Small system with low-income adder
    print("\n### EXAMPLE 2: Low-Income Residential System ###")
    results2 = calculator.calculate(
        system_size_kw=20,
        adders=['low_income']
    )
    calculator.print_results(results2)

    # Example 3: Medium commercial system with multiple adders
    print("\n### EXAMPLE 3: Commercial System with Storage ###")
    results3 = calculator.calculate(
        system_size_kw=500,
        adders=['energy_storage', 'location_based']
    )
    calculator.print_results(results3)

    # Example 4: Large ground-mount with storage requirement
    print("\n### EXAMPLE 4: Large Ground-Mount System ###")
    results4 = calculator.calculate(
        system_size_kw=2000,
        adders=['energy_storage', 'pollinator_habitat']
    )
    calculator.print_results(results4)

    # Example 5: 20-year incentive period
    print("\n### EXAMPLE 5: Commercial System with 20-Year Incentive ###")
    results5 = calculator.calculate(
        system_size_kw=750,
        adders=['energy_storage', 'location_based'],
        incentive_period_years=20
    )
    calculator.print_results(results5)

    # Show available adders
    calculator.list_available_adders()

    # Export examples
    print("\n### EXPORT TO GOOGLE SHEETS ###")
    print("\nExporting calculation results to CSV for Google Sheets...")

    # Export single calculation
    calculator.export_to_csv(results3, "commercial_system_500kw.csv", "Commercial 500kW")

    # Batch export for comparison
    all_results = [results1, results2, results3, results4, results5]
    calculator.export_batch_to_csv(all_results, "smart_comparison.csv")

    print("\nHow to use in Google Sheets:")
    print("1. Open Google Sheets (sheets.google.com)")
    print("2. File → Import → Upload → Select the CSV file")
    print("3. Choose 'Replace spreadsheet' or 'Insert new sheet(s)'")
    print("4. The data will be formatted and ready for analysis!")

    print("\nNOTE: Rates are based on PY2025 and are approximate.")
    print("For official rates, consult the Mass.gov SMART program documentation.")
    print("\nSources:")
    print("- https://www.mass.gov/info-details/smart-30-program-details")
    print("- https://www.mass.gov/doc/draft-program-year-2026-annual-report")


if __name__ == '__main__':
    main()
