import pandas as pd
import os

os.makedirs('data', exist_ok=True)

# DG CLASSES MASTER DATA

dg_classes_data = {
    'class_id': [
        '1', '1.1', '1.2', '1.3', '1.4', '1.5', '1.6',
        '2.1', '2.2', '2.3',
        '3',
        '4.1', '4.2', '4.3',
        '5.1', '5.2',
        '6.1', '6.2',
        '7',
        '8',
        '9'
    ],
    'class_name': [
        'Explosives', 'Mass Explosion', 'Projection Hazard', 'Fire Hazard', 
        'Minor Explosion', 'Very Insensitive', 'Extremely Insensitive',
        'Flammable Gases', 'Non-flammable Gases', 'Toxic Gases',
        'Flammable Liquids',
        'Flammable Solids', 'Spontaneous Combustion', 'Dangerous When Wet',
        'Oxidizing Substances', 'Organic Peroxides',
        'Toxic Substances', 'Infectious Substances',
        'Radioactive Material',
        'Corrosive Substances',
        'Miscellaneous Dangerous Goods'
    ],
    'primary_risk': [
        'Explosion', 'Mass Explosion', 'Projection/Fire', 'Fire', 
        'Minor Blast', 'Insensitive Explosion', 'Extremely Stable',
        'Fire/Explosion', 'Asphyxiation', 'Toxicity',
        'Fire',
        'Fire', 'Spontaneous Fire', 'Fire/Toxic Gas',
        'Fire Enhancement', 'Fire/Explosion',
        'Poisoning', 'Infection',
        'Radiation',
        'Chemical Burns',
        'Various'
    ],
    'description': [
        'Substances and articles with explosive properties',
        'Mass explosion hazard', 'Projection hazard but not mass explosion',
        'Fire hazard and minor blast', 'No significant hazard',
        'Very insensitive substances', 'Extremely insensitive articles',
        'Gases which are flammable at 20°C', 'Non-flammable, non-toxic gases',
        'Gases which are toxic by inhalation',
        'Liquids with flashpoint ≤60°C',
        'Flammable solids, self-reactive', 'Liable to spontaneous combustion',
        'Emit flammable gas in contact with water',
        'Oxidizing substances', 'Organic peroxides - thermally unstable',
        'Toxic substances causing death/injury', 'Pathogens - bacteria/viruses',
        'Contain radioactive isotopes',
        'Cause severe corrosion to skin/metals',
        'Other substances presenting danger'
    ],
    'general_risk_level': [
        'CRITICAL', 'CRITICAL', 'CRITICAL', 'HIGH', 
        'MEDIUM', 'LOW', 'LOW',
        'HIGH', 'MEDIUM', 'CRITICAL',
        'HIGH',
        'HIGH', 'HIGH', 'HIGH',
        'HIGH', 'CRITICAL',
        'HIGH', 'CRITICAL',
        'CRITICAL',
        'MEDIUM',
        'LOW'
    ],
    'stowage_category': [
        'B', 'B', 'B', 'B', 'A', 'A', 'A',
        'D', 'A', 'D',
        'E',
        'E', 'D', 'E',
        'B', 'D',
        'A', 'B',
        'B',
        'C',
        'A'
    ],
    'special_requirements': [
        'Explosive magazine required', 'Maximum segregation', 'Away from living quarters',
        'Keep cool and dry', 'Standard stowage', 'Standard stowage', 'Standard stowage',
        'Away from ignition sources', 'Ventilated area', 'Toxic gas warning system',
        'Away from heat/ignition',
        'Keep dry', 'Protect from heat', 'Keep away from water',
        'Away from combustibles', 'Temperature controlled',
        'Ventilation required', 'Biohazard containment',
        'Radiation monitoring',
        'Separate from foodstuffs',
        'Check compatibility'
    ]
}


# SEGREGATION RULES MATRIX
# Based on IMDG Code segregation table
segregation_rules_data = {
    'class_from': [
        # Class 1 (Explosives) segregation
        '1', '1', '1', '1', '1', '1', '1', '1', '1', '1',
        # Class 2.1 (Flammable Gas) segregation
        '2.1', '2.1', '2.1', '2.1', '2.1', '2.1', '2.1', '2.1',
        # Class 2.2 (Non-flammable Gas) segregation
        '2.2', '2.2', '2.2', '2.2', '2.2',
        # Class 2.3 (Toxic Gas) segregation
        '2.3', '2.3', '2.3', '2.3', '2.3', '2.3', '2.3', '2.3',
        # Class 3 (Flammable Liquid) segregation
        '3', '3', '3', '3', '3', '3', '3', '3',
        # Class 4.1 (Flammable Solid) segregation
        '4.1', '4.1', '4.1', '4.1', '4.1', '4.1',
        # Class 4.2 (Spontaneous Combustion) segregation
        '4.2', '4.2', '4.2', '4.2', '4.2',
        # Class 4.3 (Dangerous When Wet) segregation
        '4.3', '4.3', '4.3', '4.3', '4.3',
        # Class 5.1 (Oxidizer) segregation
        '5.1', '5.1', '5.1', '5.1', '5.1', '5.1',
        # Class 5.2 (Organic Peroxide) segregation
        '5.2', '5.2', '5.2', '5.2',
        # Class 6.1 (Toxic) segregation
        '6.1', '6.1', '6.1', '6.1',
        # Class 6.2 (Infectious) segregation
        '6.2', '6.2', '6.2',
        # Class 7 (Radioactive) segregation
        '7', '7', '7',
        # Class 8 (Corrosive) segregation
        '8', '8',
        # Class 9 (Miscellaneous) segregation
        '9'
    ],
    'class_to': [
        # Class 1 segregation
        '1.4', '2.1', '2.2', '2.3', '3', '4.1', '4.2', '4.3', '5.1', '5.2',
        # Class 2.1 segregation
        '2.1', '2.3', '3', '4.1', '4.2', '4.3', '5.1', '5.2',
        # Class 2.2 segregation
        '2.2', '3', '4.1', '5.1', '8',
        # Class 2.3 segregation
        '2.3', '3', '4.1', '4.2', '4.3', '5.1', '6.1', '8',
        # Class 3 segregation
        '3', '4.1', '4.2', '4.3', '5.1', '5.2', '8', '9',
        # Class 4.1 segregation
        '4.1', '4.2', '4.3', '5.1', '5.2', '8',
        # Class 4.2 segregation
        '4.2', '4.3', '5.1', '5.2', '8',
        # Class 4.3 segregation
        '4.3', '5.1', '5.2', '6.1', '8',
        # Class 5.1 segregation
        '5.1', '5.2', '6.1', '8', '9', '6.2',
        # Class 5.2 segregation
        '5.2', '6.1', '8', '9',
        # Class 6.1 segregation
        '6.1', '6.2', '8', '9',
        # Class 6.2 segregation
        '6.2', '8', '9',
        # Class 7 segregation
        '7', '8', '9',
        # Class 8 segregation
        '8', '9',
        # Class 9 segregation
        '9'
    ],
    'segregation_code': [
        # Class 1
        '2', '4', '2', '4', '4', '4', '4', '4', '4', '4',
        # Class 2.1
        'X', '2', '2', '2', '2', '2', '4', '4',
        # Class 2.2
        'X', '1', '1', '1', 'X',
        # Class 2.3
        'X', '2', '2', '2', '2', '2', '1', '2',
        # Class 3
        'X', '2', '2', '2', '4', '4', '1', 'X',
        # Class 4.1
        'X', '1', '1', '4', '4', '2',
        # Class 4.2
        'X', '1', '4', '4', '2',
        # Class 4.3
        'X', '4', '4', '2', '2',
        # Class 5.1
        'X', '4', '2', '2', '1', '2',
        # Class 5.2
        'X', '2', '2', '1',
        # Class 6.1
        'X', '3', '1', 'X',
        # Class 6.2
        'X', '2', 'X',
        # Class 7
        'X', '2', '1',
        # Class 8
        'X', 'X',
        # Class 9
        'X'
    ],
    'segregation_rule': [
        # Class 1
        'Away from (3m minimum)', 'Separated from (separate holds)', 
        'Away from (3m minimum)', 'Separated from', 'Separated from',
        'Separated from', 'Separated from', 'Separated from', 'Separated from', 'Separated from',
        # Class 2.1
        'Can be stowed together', 'Away from (3m minimum)', 'Away from (3m minimum)',
        'Away from (3m minimum)', 'Away from (3m minimum)', 'Away from (3m minimum)',
        'Separated from', 'Separated from',
        # Class 2.2
        'Can be stowed together', 'Away from (1.5m minimum)', 'Away from (1.5m minimum)',
        'Away from (1.5m minimum)', 'Can be stowed together',
        # Class 2.3
        'Can be stowed together', 'Away from (3m minimum)', 'Away from (3m minimum)',
        'Away from (3m minimum)', 'Away from (3m minimum)', 'Away from (3m minimum)',
        'Away from (1.5m minimum)', 'Away from (3m minimum)',
        # Class 3
        'Can be stowed together', 'Away from (3m minimum)', 'Away from (3m minimum)',
        'Away from (3m minimum)', 'Separated from', 'Separated from',
        'Away from (1.5m minimum)', 'Can be stowed together',
        # Class 4.1
        'Can be stowed together', 'Away from (1.5m minimum)', 'Away from (1.5m minimum)',
        'Separated from', 'Separated from', 'Away from (3m minimum)',
        # Class 4.2
        'Can be stowed together', 'Away from (1.5m minimum)', 'Separated from',
        'Separated from', 'Away from (3m minimum)',
        # Class 4.3
        'Can be stowed together', 'Separated from', 'Separated from',
        'Away from (3m minimum)', 'Away from (3m minimum)',
        # Class 5.1
        'Can be stowed together', 'Separated from', 'Away from (3m minimum)',
        'Away from (3m minimum)', 'Away from (1.5m minimum)', 'Away from (3m minimum)',
        # Class 5.2
        'Can be stowed together', 'Away from (3m minimum)', 'Away from (3m minimum)',
        'Away from (1.5m minimum)',
        # Class 6.1
        'Can be stowed together', 'Separated by (one compartment)', 'Away from (1.5m minimum)',
        'Can be stowed together',
        # Class 6.2
        'Can be stowed together', 'Away from (3m minimum)', 'Can be stowed together',
        # Class 7
        'Can be stowed together', 'Away from (3m minimum)', 'Away from (1.5m minimum)',
        # Class 8
        'Can be stowed together', 'Can be stowed together',
        # Class 9
        'Can be stowed together'
    ],
    'risk_penalty': [
        # Class 1
        10, 25, 10, 25, 25, 25, 25, 25, 25, 25,
        # Class 2.1
        0, 10, 10, 10, 10, 10, 25, 25,
        # Class 2.2
        0, 5, 5, 5, 0,
        # Class 2.3
        0, 10, 10, 10, 10, 10, 5, 10,
        # Class 3
        0, 10, 10, 10, 25, 25, 5, 0,
        # Class 4.1
        0, 5, 5, 25, 25, 10,
        # Class 4.2
        0, 5, 25, 25, 10,
        # Class 4.3
        0, 25, 25, 10, 10,
        # Class 5.1
        0, 25, 10, 10, 5, 10,
        # Class 5.2
        0, 10, 10, 5,
        # Class 6.1
        0, 15, 5, 0,
        # Class 6.2
        0, 10, 0,
        # Class 7
        0, 10, 5,
        # Class 8
        0, 0,
        # Class 9
        0
    ]
}



df_classes = pd.DataFrame(dg_classes_data)
df_segregation = pd.DataFrame(segregation_rules_data)

if os.path.isfile("/data/dg_classes.json"):
    print ("dg_classes .json already exists")
else:
    df_classes.to_json('data/dg_classes.json', orient='records', indent=4)
    print("dg_classes .json made successfully")



if os.path.isfile("/data/segregation_rules.json"):
    print ("segregation_rules.json already exists")
else:
    df_segregation.to_json('data/segregation_rules.json', orient='records', indent=4)
    print("segregation_rules.json created successfully")