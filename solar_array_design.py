#!/usr/bin/env python3
"""
Solar Array Design Tool
-----------------------
Designs a solar PV system to offset 105% of annual electricity consumption
for 173R High St Shop, Waltham, MA (Eversource East).

Based on 12-month utility bill history takeoff.
"""

# =============================================================================
# CLIENT & SITE INFORMATION
# =============================================================================
CLIENT_INFO = {
    "esco_client": "EnergySource",
    "facility_address": "173R High St Shop, Waltham, MA",
    "electric_utility": "Eversource East",
    "account_number": "74011537649",
    "latitude": 42.3765,
    "longitude": -71.2356,
}

# =============================================================================
# 12-MONTH BILL HISTORY (kWh)
# =============================================================================
MONTHLY_CONSUMPTION = {
    "Jan": 2559,
    "Feb": 2745,
    "Mar": 2338,
    "Apr": 2375,
    "May": 2353,
    "Jun": 1732,
    "Jul": 1773,
    "Aug": 2949,
    "Sep": 1783,
    "Oct": 1547,
    "Nov": 2046,
    "Dec": 2431,
}

# =============================================================================
# UTILITY RATE STRUCTURE
# =============================================================================
RATES = {
    "supply_rate": 0.159,       # $/kWh
    "delivery_rate": 0.130,     # $/kWh
    "retail_rate": 0.289,       # $/kWh (supply + delivery)
    "discount_rate": 0.02,      # 2% general inflation
    "rate_escalator": 0.05,     # 5% annual rate hike
}

# =============================================================================
# SOLAR DESIGN PARAMETERS
# =============================================================================
OFFSET_TARGET = 1.05  # 105% offset

# Waltham, MA - Monthly peak sun hours (kWh/m²/day) for south-facing
# fixed-tilt system at ~25-30° tilt (NREL TMY3 / PVWatts data for Boston area)
MONTHLY_PEAK_SUN_HOURS = {
    "Jan": 2.79,
    "Feb": 3.48,
    "Mar": 4.26,
    "Apr": 4.83,
    "May": 5.34,
    "Jun": 5.72,
    "Jul": 5.63,
    "Aug": 5.17,
    "Sep": 4.38,
    "Oct": 3.42,
    "Nov": 2.55,
    "Dec": 2.35,
}

DAYS_IN_MONTH = {
    "Jan": 31, "Feb": 28, "Mar": 31, "Apr": 30,
    "May": 31, "Jun": 30, "Jul": 31, "Aug": 31,
    "Sep": 30, "Oct": 31, "Nov": 30, "Dec": 31,
}

# System losses / performance ratio
SYSTEM_LOSSES = {
    "inverter_efficiency": 0.966,
    "wiring_losses": 0.98,
    "soiling": 0.98,
    "shading": 0.97,
    "snow": 0.95,        # Waltham, MA gets winter snow
    "mismatch": 0.98,
    "availability": 0.99,
    "temperature_derate": 0.94,  # Annual average for MA climate
}

# Equipment specifications
PANEL_SPEC = {
    "manufacturer": "REC",
    "model": "REC Alpha Pure-R 430W",
    "wattage_stc": 430,          # Watts STC
    "efficiency": 0.220,          # 22.0% module efficiency
    "dimensions_mm": (1821, 1016, 30),  # L x W x H in mm
    "area_sqft": 20.3,           # per panel
    "warranty_years": 25,
    "degradation_yr1": 0.02,     # 2% first year
    "degradation_annual": 0.004, # 0.4% per year after
    "temp_coeff_pmax": -0.0026,  # -0.26%/°C
}

INVERTER_SPEC = {
    "manufacturer": "Enphase",
    "model": "IQ8A Microinverter",
    "rated_power_w": 366,         # Continuous AC output
    "peak_power_w": 430,          # Peak AC power
    "max_dc_input_w": 480,        # Max DC input
    "efficiency": 0.972,          # CEC weighted efficiency
    "warranty_years": 25,
}

# Financial assumptions
FINANCIAL = {
    "cost_per_watt_dc": 3.10,    # Installed cost $/Wdc (commercial, MA)
    "federal_itc": 0.30,          # 30% federal ITC
    "state_incentive_per_w": 0.0, # MA SMART program (varies by capacity block)
    "smart_rate_kwh": 0.08,       # Estimated MA SMART incentive $/kWh
    "smart_term_years": 20,       # SMART program term
    "annual_maintenance": 0.01,   # 1% of system cost per year
    "analysis_period_years": 25,
}


def calculate_performance_ratio():
    """Calculate overall system performance ratio from individual losses."""
    pr = 1.0
    for factor in SYSTEM_LOSSES.values():
        pr *= factor
    return pr


def design_system():
    """Design the solar array and return all specifications."""
    # -------------------------------------------------------------------------
    # 1. CONSUMPTION ANALYSIS
    # -------------------------------------------------------------------------
    annual_consumption = sum(MONTHLY_CONSUMPTION.values())
    target_production = annual_consumption * OFFSET_TARGET
    annual_cost = annual_consumption * RATES["retail_rate"]
    avg_monthly = annual_consumption / 12

    # -------------------------------------------------------------------------
    # 2. SYSTEM SIZING
    # -------------------------------------------------------------------------
    performance_ratio = calculate_performance_ratio()

    # Calculate annual peak sun hours
    annual_psh = sum(
        MONTHLY_PEAK_SUN_HOURS[m] * DAYS_IN_MONTH[m]
        for m in MONTHLY_PEAK_SUN_HOURS
    )

    # System size calculation: target_kWh / (PSH * PR)
    # production = system_kw * annual_psh * performance_ratio
    system_size_kw = target_production / (annual_psh * performance_ratio)

    # Panel count
    panels_exact = (system_size_kw * 1000) / PANEL_SPEC["wattage_stc"]
    num_panels = int(panels_exact) + (1 if panels_exact % 1 > 0 else 0)

    # Actual system size based on panel count
    actual_system_kw = (num_panels * PANEL_SPEC["wattage_stc"]) / 1000
    actual_production = actual_system_kw * annual_psh * performance_ratio

    # Microinverters (1:1 ratio with panels)
    num_inverters = num_panels

    # -------------------------------------------------------------------------
    # 3. MONTHLY PRODUCTION ESTIMATE
    # -------------------------------------------------------------------------
    monthly_production = {}
    for month in MONTHLY_CONSUMPTION:
        psh = MONTHLY_PEAK_SUN_HOURS[month]
        days = DAYS_IN_MONTH[month]
        monthly_kwh = actual_system_kw * psh * days * performance_ratio
        monthly_production[month] = round(monthly_kwh, 1)

    # -------------------------------------------------------------------------
    # 4. ARRAY LAYOUT
    # -------------------------------------------------------------------------
    total_array_sqft = num_panels * PANEL_SPEC["area_sqft"]

    # Typical commercial roof layout: portrait orientation, 2-up racking
    # Row spacing at 42°N latitude for minimal shading (Dec 21 sun angle)
    row_spacing_ft = 5.0  # feet between rows for tilt racks
    panel_w_ft = PANEL_SPEC["dimensions_mm"][1] / 304.8  # ~3.33 ft
    panel_l_ft = PANEL_SPEC["dimensions_mm"][0] / 304.8  # ~5.97 ft

    # Portrait, 2-up configuration
    panels_per_row_pair = 2
    num_strings = num_panels // panels_per_row_pair
    remaining = num_panels % panels_per_row_pair

    # -------------------------------------------------------------------------
    # 5. FINANCIAL ANALYSIS
    # -------------------------------------------------------------------------
    gross_cost = actual_system_kw * 1000 * FINANCIAL["cost_per_watt_dc"]
    federal_itc = gross_cost * FINANCIAL["federal_itc"]
    net_cost = gross_cost - federal_itc

    # Year 1 savings
    year1_production = actual_production * (1 - PANEL_SPEC["degradation_yr1"])
    year1_savings = year1_production * RATES["retail_rate"]
    year1_smart = year1_production * FINANCIAL["smart_rate_kwh"]
    year1_total_benefit = year1_savings + year1_smart
    annual_maint = gross_cost * FINANCIAL["annual_maintenance"]

    # 25-year cash flow
    cumulative_savings = 0.0
    payback_year = None
    cash_flows = []
    current_rate = RATES["retail_rate"]
    production = actual_production

    for year in range(1, FINANCIAL["analysis_period_years"] + 1):
        # Degradation
        if year == 1:
            production = actual_production * (1 - PANEL_SPEC["degradation_yr1"])
        else:
            production = production * (1 - PANEL_SPEC["degradation_annual"])

        # Rate escalation
        if year > 1:
            current_rate *= (1 + RATES["rate_escalator"])

        energy_savings = production * current_rate
        smart_income = production * FINANCIAL["smart_rate_kwh"] if year <= FINANCIAL["smart_term_years"] else 0
        maint = annual_maint * ((1 + RATES["discount_rate"]) ** (year - 1))

        net_benefit = energy_savings + smart_income - maint
        cumulative_savings += net_benefit

        if payback_year is None and cumulative_savings >= net_cost:
            payback_year = year

        cash_flows.append({
            "year": year,
            "production_kwh": round(production, 0),
            "rate": round(current_rate, 4),
            "energy_savings": round(energy_savings, 2),
            "smart_income": round(smart_income, 2),
            "maintenance": round(maint, 2),
            "net_benefit": round(net_benefit, 2),
            "cumulative": round(cumulative_savings, 2),
        })

    total_25yr_savings = cumulative_savings
    roi = ((total_25yr_savings - net_cost) / net_cost) * 100
    lcoe = net_cost / sum(cf["production_kwh"] for cf in cash_flows)

    return {
        "consumption": {
            "monthly": MONTHLY_CONSUMPTION,
            "annual_kwh": annual_consumption,
            "target_kwh": round(target_production, 1),
            "annual_cost": round(annual_cost, 2),
            "avg_monthly_kwh": round(avg_monthly, 1),
        },
        "system": {
            "size_kw_dc": round(actual_system_kw, 2),
            "num_panels": num_panels,
            "panel": PANEL_SPEC,
            "num_inverters": num_inverters,
            "inverter": INVERTER_SPEC,
            "performance_ratio": round(performance_ratio, 4),
            "annual_psh": round(annual_psh, 1),
            "tilt_deg": 27,
            "azimuth_deg": 180,  # Due south
        },
        "production": {
            "monthly": monthly_production,
            "annual_kwh": round(actual_production, 1),
            "year1_kwh": round(year1_production, 1),
            "offset_pct": round((actual_production / annual_consumption) * 100, 1),
        },
        "layout": {
            "total_array_sqft": round(total_array_sqft, 1),
            "panel_dimensions_ft": (round(panel_l_ft, 2), round(panel_w_ft, 2)),
            "orientation": "Portrait, 2-up racking",
            "row_spacing_ft": row_spacing_ft,
        },
        "financial": {
            "gross_cost": round(gross_cost, 2),
            "federal_itc": round(federal_itc, 2),
            "net_cost": round(net_cost, 2),
            "cost_per_watt": FINANCIAL["cost_per_watt_dc"],
            "year1_savings": round(year1_savings, 2),
            "year1_smart": round(year1_smart, 2),
            "year1_total_benefit": round(year1_total_benefit, 2),
            "payback_years": payback_year,
            "total_25yr_savings": round(total_25yr_savings, 2),
            "roi_pct": round(roi, 1),
            "lcoe": round(lcoe, 4),
            "cash_flows": cash_flows,
        },
    }


def print_report(design):
    """Print a formatted solar design report."""
    c = design["consumption"]
    s = design["system"]
    p = design["production"]
    la = design["layout"]
    f = design["financial"]

    print("=" * 72)
    print("           SOLAR ARRAY DESIGN PROPOSAL")
    print("=" * 72)
    print()
    print(f"  Client:      {CLIENT_INFO['esco_client']}")
    print(f"  Facility:    {CLIENT_INFO['facility_address']}")
    print(f"  Utility:     {CLIENT_INFO['electric_utility']}")
    print(f"  Account:     {CLIENT_INFO['account_number']}")
    print(f"  Coordinates: {CLIENT_INFO['latitude']}°N, {abs(CLIENT_INFO['longitude'])}°W")
    print()

    # --- CONSUMPTION TAKEOFF ---
    print("-" * 72)
    print("  1. CONSUMPTION TAKEOFF (12-Month Bill History)")
    print("-" * 72)
    print()
    print(f"  {'Month':<8} {'Consumption (kWh)':>18} {'Cost @ $0.289':>14}")
    print(f"  {'─' * 8} {'─' * 18} {'─' * 14}")
    for month, kwh in c["monthly"].items():
        cost = kwh * RATES["retail_rate"]
        print(f"  {month:<8} {kwh:>14,} kWh  ${cost:>10,.2f}")
    print(f"  {'─' * 8} {'─' * 18} {'─' * 14}")
    print(f"  {'TOTAL':<8} {c['annual_kwh']:>14,} kWh  ${c['annual_cost']:>10,.2f}")
    print(f"  {'AVG/MO':<8} {c['avg_monthly_kwh']:>14,.1f} kWh")
    print()
    print(f"  Target Production (105%): {c['target_kwh']:,.1f} kWh/yr")
    print()

    # --- SYSTEM DESIGN ---
    print("-" * 72)
    print("  2. SYSTEM DESIGN")
    print("-" * 72)
    print()
    print(f"  System Size (DC):      {s['size_kw_dc']:.2f} kWdc")
    print(f"  Number of Panels:      {s['num_panels']}")
    print(f"  Panel:                 {s['panel']['manufacturer']} {s['panel']['model']}")
    print(f"  Panel Wattage:         {s['panel']['wattage_stc']}W STC")
    print(f"  Panel Efficiency:      {s['panel']['efficiency'] * 100:.1f}%")
    print(f"  Inverter:              {s['inverter']['manufacturer']} {s['inverter']['model']}")
    print(f"  Inverter Count:        {s['num_inverters']} (1:1 micro)")
    print(f"  Inverter Efficiency:   {s['inverter']['efficiency'] * 100:.1f}% CEC")
    print(f"  Array Tilt:            {s['tilt_deg']}°")
    print(f"  Array Azimuth:         {s['azimuth_deg']}° (due south)")
    print(f"  Performance Ratio:     {s['performance_ratio']:.2%}")
    print(f"  Annual Peak Sun Hours: {s['annual_psh']:.1f} hrs")
    print()

    # --- ARRAY LAYOUT ---
    print("-" * 72)
    print("  3. ARRAY LAYOUT")
    print("-" * 72)
    print()
    print(f"  Total Array Area:      {la['total_array_sqft']:,.1f} sq ft")
    print(f"  Panel Dimensions:      {la['panel_dimensions_ft'][0]:.1f}' x {la['panel_dimensions_ft'][1]:.1f}'")
    print(f"  Mounting:              {la['orientation']}")
    print(f"  Row Spacing:           {la['row_spacing_ft']:.1f} ft (tilt rack)")
    print()

    # --- PRODUCTION ESTIMATE ---
    print("-" * 72)
    print("  4. MONTHLY PRODUCTION ESTIMATE")
    print("-" * 72)
    print()
    print(f"  {'Month':<8} {'Consumption':>12} {'Production':>12} {'Net':>10} {'Offset':>8}")
    print(f"  {'─' * 8} {'─' * 12} {'─' * 12} {'─' * 10} {'─' * 8}")
    total_prod = 0
    for month in c["monthly"]:
        cons = c["monthly"][month]
        prod = p["monthly"][month]
        net = prod - cons
        offset = (prod / cons) * 100 if cons > 0 else 0
        total_prod += prod
        sign = "+" if net >= 0 else ""
        print(f"  {month:<8} {cons:>9,} kWh {prod:>9,.1f} kWh {sign}{net:>7,.1f} kWh {offset:>6.1f}%")
    print(f"  {'─' * 8} {'─' * 12} {'─' * 12} {'─' * 10} {'─' * 8}")
    net_total = total_prod - c["annual_kwh"]
    print(f"  {'TOTAL':<8} {c['annual_kwh']:>9,} kWh {total_prod:>9,.1f} kWh +{net_total:>6,.1f} kWh {p['offset_pct']:>6.1f}%")
    print()
    print(f"  Year 1 Production (after degradation): {p['year1_kwh']:,.1f} kWh")
    print()

    # --- FINANCIAL ANALYSIS ---
    print("-" * 72)
    print("  5. FINANCIAL ANALYSIS")
    print("-" * 72)
    print()
    print(f"  Gross System Cost:     ${f['gross_cost']:>12,.2f}  ({f['cost_per_watt']:.2f}/Wdc)")
    print(f"  Federal ITC (30%):    -${f['federal_itc']:>12,.2f}")
    print(f"  ─────────────────────────────────────")
    print(f"  Net System Cost:       ${f['net_cost']:>12,.2f}")
    print()
    print(f"  Year 1 Energy Savings: ${f['year1_savings']:>12,.2f}")
    print(f"  Year 1 SMART Income:   ${f['year1_smart']:>12,.2f}")
    print(f"  Year 1 Total Benefit:  ${f['year1_total_benefit']:>12,.2f}")
    print()
    print(f"  Simple Payback:        {f['payback_years']} years")
    print(f"  25-Year Net Savings:   ${f['total_25yr_savings']:>12,.2f}")
    print(f"  25-Year ROI:           {f['roi_pct']:.1f}%")
    print(f"  LCOE:                  ${f['lcoe']:.4f}/kWh")
    print()

    # --- 25-YEAR CASH FLOW ---
    print("-" * 72)
    print("  6. 25-YEAR CASH FLOW PROJECTION")
    print("-" * 72)
    print()
    print(f"  {'Yr':>3}  {'Prod (kWh)':>11}  {'Rate':>7}  {'Savings':>10}  {'SMART':>8}  {'Maint':>8}  {'Net':>10}  {'Cumul.':>12}")
    print(f"  {'─' * 3}  {'─' * 11}  {'─' * 7}  {'─' * 10}  {'─' * 8}  {'─' * 8}  {'─' * 10}  {'─' * 12}")
    for cf in f["cash_flows"]:
        payback_marker = " ◄" if cf["year"] == f["payback_years"] else ""
        print(
            f"  {cf['year']:>3}  {cf['production_kwh']:>9,.0f}  "
            f"${cf['rate']:>.4f}  ${cf['energy_savings']:>9,.2f}  "
            f"${cf['smart_income']:>7,.2f}  ${cf['maintenance']:>7,.2f}  "
            f"${cf['net_benefit']:>9,.2f}  ${cf['cumulative']:>11,.2f}{payback_marker}"
        )
    print()

    # --- SUMMARY ---
    print("=" * 72)
    print("  DESIGN SUMMARY")
    print("=" * 72)
    print()
    print(f"  System:  {s['size_kw_dc']:.2f} kWdc  |  {s['num_panels']} x {s['panel']['wattage_stc']}W panels  |  Enphase IQ8A micros")
    print(f"  Output:  {p['annual_kwh']:,.1f} kWh/yr  |  {p['offset_pct']:.1f}% offset  |  {p['year1_kwh']:,.1f} kWh Yr1")
    print(f"  Cost:    ${f['net_cost']:,.2f} net  |  {f['payback_years']} yr payback  |  {f['roi_pct']:.1f}% 25yr ROI")
    print()
    print("  Notes:")
    print("  - Production estimates based on NREL TMY3 data for Boston/Waltham, MA")
    print("  - Performance ratio includes snow loss factor for New England climate")
    print("  - MA SMART incentive estimated at $0.08/kWh for 20 years")
    print("  - Rate escalation assumed at 5% annually per utility trend")
    print("  - Site survey required to confirm roof condition, shading, and orientation")
    print("  - Structural engineering review recommended for commercial roof loading")
    print("  - Interconnection application required with Eversource East")
    print()
    print("=" * 72)


if __name__ == "__main__":
    design = design_system()
    print_report(design)
