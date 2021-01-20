import math

u0 = 0.00000125663706212
core_types = {
    'STEEL10': {"ur": 5000, "bsat": 1.0},
    'STEEL13': {"ur": 4000, "bsat": 1.3},
    'STEEL16': {"ur": 3000, "bsat": 1.6},
    '3C11': {"ur": 4300, "bsat": 0.23},
    '3C81': {"ur": 2700, "bsat": 0.36},
    '3C90': {"ur": 2300, "bsat": 0.38},
    '3C91': {"ur": 3000, "bsat": 0.37},
    '3C92': {"ur": 1500, "bsat": 0.46},
    '3C93': {"ur": 1800, "bsat": 0.43},
    '3C94': {"ur": 2300, "bsat": 0.38},
    '3C95': {"ur": 3000, "bsat": 0.41},
    '3C96': {"ur": 2000, "bsat": 0.44},
    '3C97': {"ur": 3000, "bsat": 0.41},
    '3C98': {"ur": 2500, "bsat": 0.44},
    '3E5': {"ur": 10000, "bsat": 0.23},
    '3E6': {"ur": 12000, "bsat": 0.22},
    '3E7': {"ur": 15000, "bsat": 0.22},
    '3E8': {"ur": 18000, "bsat": 0.21},
    '3E10': {"ur": 10000, "bsat": 0.27},
    '3E12': {"ur": 12000, "bsat": 0.29},
    '3E25': {"ur": 6000, "bsat": 0.22},
    '3E26': {"ur": 7000, "bsat": 0.30},
    '3E27': {"ur": 6000, "bsat": 0.27},
    '3E28': {"ur": 4000, "bsat": 0.28},
    '3F3': {"ur": 2000, "bsat": 0.37},
    '3R1': {"ur": 800, "bsat": 0.34},
    '4C65': {"ur": 125, "bsat": 0.34},
    'M33': {"ur": 750, "bsat": 0.31},
    'N27': {"ur": 2000, "bsat": 0.41},
    'N30': {"ur": 4300, "bsat": 0.24},
    'N48': {"ur": 2300, "bsat": 0.31},
    'N87': {"ur": 2200, "bsat": 0.39},
    'N95': {"ur": 3000, "bsat": 0.41},
    'N97': {"ur": 2300, "bsat": 0.41},
    'T35': {"ur": 6000, "bsat": 0.27},
    'T36': {"ur": 7000, "bsat": 0.24},
    'T37': {"ur": 6500, "bsat": 0.24},
    'T38': {"ur": 10000, "bsat": 0.26}
}


# Ae - area of cross section which will condut mag. flux
def toroid_cross_section_area(length, outer, inner):
    return ((outer - inner) / 2) * length


# le - length of path for mag. flux
def toroid_magnetic_path_length(outer, inner):

    return math.pi * (outer - (outer - inner) / 2)


# Al - approx. inductance factor varying +- 25%
# can be used to estimate inductance of inductor as L = N^2 * Al
# where N is amount of turns
def toroid_inductance_factor(ue, length, outer, inner):
    return u0 * \
           ue * \
           (toroid_cross_section_area(length, outer, inner) / toroid_magnetic_path_length(outer, inner))


def toroid_one_loop_len(depth, outer, inner):
    return (outer - inner) + 2 * depth


# tor_length = 13.6 / 1000
# tor_outer_diameter = 43.6 / 1000
# tor_inner_diameter = 24.8 / 1000

# set uncoated values B64290L0022X830 EPCOS
tor_depth = 12.5 / 1000
tor_outer_diameter = 41.8 / 1000
tor_inner_diameter = 26.2 / 1000
core_type = 'N30'
inductance_coefficient = 5000  # nH
voltage_primary = 20
voltage_secondary = 40
frequency = 10000

halfWaveDuration = 1/(2*frequency)
hbridgePulseDeadtime = halfWaveDuration * 0.1  # 10% dead time of single pulse
hbridgePulseLength = halfWaveDuration - hbridgePulseDeadtime

relative_permeability = core_types[core_type]['ur']  # μe
bsat = core_types[core_type]['bsat']
bmax = bsat * 0.75

loop_length = toroid_one_loop_len(tor_depth, tor_outer_diameter, tor_inner_diameter)
cross_section = toroid_cross_section_area(tor_depth, tor_outer_diameter, tor_inner_diameter)
mag_path_len = toroid_magnetic_path_length(tor_outer_diameter, tor_inner_diameter)

max_magnetic_flux = cross_section * bmax

# TODO cores with air gap are calculated μe = μr * le / (le + (g * μr))
effective_permeability = relative_permeability

turns_primary = voltage_primary / (4 * max_magnetic_flux * frequency)
inductance_primary = turns_primary * turns_primary * inductance_coefficient / 1000000000
impedance_primary = 2 * math.pi * frequency * inductance_primary

turns_secondary = voltage_secondary / voltage_primary * turns_primary
inductance_secondary = turns_secondary * turns_secondary * inductance_coefficient / 1000000000
# impedance_secondary = 2 * math.pi * frequency * inductance_secondary

print(f'|---Core')
print(f'| Cross section area \tAe = {cross_section * 1000000:.3f} [mm2]')
print(f'| Length of mag. path \tle = {mag_path_len * 1000:.3f} [mm]')
print(f'| Core relative permeability \tμr = {relative_permeability}')
print(f'| Core effective permeability \tμe = {effective_permeability}')
print(f'| Max mag. flux density in core \tBmax = {bmax} [T]')
print(f'| Max mag. flux during Bmax \tΦ = {max_magnetic_flux} [Wb]')
print(f'| One loop wire length = {round(loop_length * 1000, 2)} [mm]')

print('|---Primary winding')
print(f'| Turns \tNp = {round(turns_primary, 2)}')
print(f'| Primary inductance \tLp = {inductance_primary * 1000000:.3f} [μH]')
print(f'| Primary impedance \tZp = {impedance_primary:.3f} [Ω]')
print(f'| Primary winding wire length = {round(loop_length * 1000 * turns_primary, 2)} [mm]')

print('|---Secondary winding')
print(f'| Turns \tNs = {round(turns_secondary, 2)}')
print(f'| Secondary inductance \tLs = {inductance_secondary * 1000000:.3f} [μH]')
print(f'| Secondary winding wire length = {round(loop_length * 1000 * turns_secondary, 2)} [mm]')
print('---------------')
