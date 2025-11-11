import pandas as pd
import random
import os




# Class-specific naming templates
class_templates = {
    '1.1': {
        'prefixes': ['Explosive', 'Dynamite', 'TNT', 'Detonator', 'Ammunition', 'Primer', 'Charge'],
        'suffixes': ['type A', 'type B', 'with burster', 'blasting', 'military', 'commercial', 'shaped'],
        'uses': ['Mining', 'Military', 'Construction', 'Demolition', 'Quarrying'],
        'provisions': ['Explosive magazine required', 'Maximum segregation', 'No smoking zones', 'Shock-sensitive']
    },
    '1.2': {
        'prefixes': ['Explosive', 'Projectile', 'Rocket', 'Warhead', 'Missile'],
        'suffixes': ['with charge', 'inert loaded', 'training', 'practice', 'illuminating'],
        'uses': ['Military training', 'Defense', 'Aerospace', 'Pyrotechnics'],
        'provisions': ['Projection hazard', 'Separation required', 'Shock-sensitive', 'Fire risk']
    },
    '1.3': {
        'prefixes': ['Explosive', 'Propellant', 'Rocket motor', 'Ammunition'],
        'suffixes': ['smokeless', 'with expelling charge', 'igniter', 'primer'],
        'uses': ['Ammunition', 'Propulsion', 'Aerospace', 'Military'],
        'provisions': ['Fire hazard', 'Keep cool', 'Away from heat', 'Minor blast risk']
    },
    '1.4': {
        'prefixes': ['Signal', 'Firework', 'Flare', 'Cartridge', 'Squib'],
        'suffixes': ['hand', 'smoke', 'illuminating', 'practice', 'blank'],
        'uses': ['Emergency signaling', 'Entertainment', 'Training', 'Safety'],
        'provisions': ['Minor hazard', 'Compatible with general cargo', 'Keep dry']
    },
    '2.1': {
        'prefixes': ['Butane', 'Propane', 'Methane', 'Ethane', 'Acetylene', 'Hydrogen', 'LPG'],
        'suffixes': ['compressed', 'liquefied', 'mixture', 'refrigerated', 'dissolved'],
        'uses': ['Fuel', 'Refrigeration', 'Welding', 'Industrial', 'Heating'],
        'provisions': ['Highly flammable', 'No ignition sources', 'Ventilation required', 'Pressure hazard']
    },
    '2.2': {
        'prefixes': ['Nitrogen', 'Oxygen', 'Carbon dioxide', 'Argon', 'Helium', 'Air'],
        'suffixes': ['compressed', 'liquefied', 'refrigerated', 'cryogenic'],
        'uses': ['Industrial', 'Medical', 'Food preservation', 'Inert atmosphere', 'Welding'],
        'provisions': ['Pressure hazard', 'Asphyxiation risk', 'Temperature control', 'Ventilation']
    },
    '2.3': {
        'prefixes': ['Chlorine', 'Ammonia', 'Sulfur dioxide', 'Hydrogen sulfide', 'Phosgene', 'Carbon monoxide'],
        'suffixes': ['anhydrous', 'compressed', 'liquefied', 'refrigerated'],
        'uses': ['Chemical production', 'Water treatment', 'Refrigeration', 'Industrial'],
        'provisions': ['Toxic by inhalation', 'Leak detection required', 'Emergency procedures', 'Respiratory protection']
    },
    '3': {
        'prefixes': ['Acetone', 'Ethanol', 'Methanol', 'Gasoline', 'Diesel', 'Paint', 'Adhesive', 'Ink', 'Solvent', 'Toluene'],
        'suffixes': ['mixture', 'solution', 'n.o.s.', 'containing', 'flammable'],
        'uses': ['Solvent', 'Fuel', 'Coating', 'Cleaning', 'Manufacturing', 'Printing'],
        'provisions': ['Flammable liquid', 'Away from heat', 'No smoking', 'Bonding/grounding required']
    },
    '4.1': {
        'prefixes': ['Sulfur', 'Matches', 'Metal powder', 'Nitrocellulose', 'Phosphorus'],
        'suffixes': ['flammable', 'self-reactive', 'organic', 'stabilized', 'wetted'],
        'uses': ['Chemical production', 'Pyrotechnics', 'Manufacturing', 'Agriculture'],
        'provisions': ['Flammable solid', 'Keep dry', 'Away from heat', 'Friction-sensitive']
    },
    '4.2': {
        'prefixes': ['Phosphorus', 'Activated carbon', 'Metal powder', 'Fishmeal', 'Coal'],
        'suffixes': ['white', 'yellow', 'pyrophoric', 'self-heating', 'stabilized'],
        'uses': ['Chemical production', 'Agriculture', 'Manufacturing', 'Industrial'],
        'provisions': ['Spontaneous combustion', 'Protect from heat', 'Temperature monitoring', 'No organic material']
    },
    '4.3': {
        'prefixes': ['Sodium', 'Potassium', 'Calcium', 'Lithium', 'Aluminum powder', 'Zinc powder'],
        'suffixes': ['metal', 'alloy', 'powder', 'hydride', 'mixture'],
        'uses': ['Chemical production', 'Metallurgy', 'Battery manufacturing', 'Industrial'],
        'provisions': ['Water-reactive', 'Keep absolutely dry', 'Emit flammable gas', 'No water for fire']
    },
    '5.1': {
        'prefixes': ['Ammonium nitrate', 'Hydrogen peroxide', 'Sodium chlorate', 'Potassium permanganate', 'Calcium hypochlorite'],
        'suffixes': ['solution', 'mixture', 'fertilizer grade', 'oxidizing', 'solid'],
        'uses': ['Fertilizer', 'Bleaching', 'Water treatment', 'Chemical production', 'Disinfection'],
        'provisions': ['Oxidizing substance', 'Away from combustibles', 'Fire enhancement', 'Separate from organics']
    },
    '5.2': {
        'prefixes': ['Organic peroxide', 'Benzoyl peroxide', 'Methyl ethyl ketone peroxide'],
        'suffixes': ['type A', 'type B', 'type C', 'type D', 'type E', 'type F', 'stabilized'],
        'uses': ['Plastics production', 'Polymerization', 'Chemical synthesis', 'Manufacturing'],
        'provisions': ['Thermally unstable', 'Temperature controlled', 'May explode', 'Refrigeration required']
    },
    '6.1': {
        'prefixes': ['Arsenic', 'Cyanide', 'Pesticide', 'Mercury', 'Lead compound', 'Nicotine', 'Strychnine'],
        'suffixes': ['solution', 'solid', 'liquid', 'compound', 'preparation', 'mixture'],
        'uses': ['Pesticide', 'Chemical production', 'Manufacturing', 'Laboratory', 'Industrial'],
        'provisions': ['Toxic substance', 'Avoid inhalation', 'Skin protection', 'Fatal if swallowed']
    },
    '6.2': {
        'prefixes': ['Infectious substance', 'Clinical waste', 'Medical waste', 'Biological substance', 'Diagnostic specimen'],
        'suffixes': ['human', 'animal', 'unspecified', 'Category A', 'Category B'],
        'uses': ['Medical diagnostics', 'Research', 'Healthcare', 'Veterinary', 'Laboratory'],
        'provisions': ['Biohazard', 'Special packaging', 'Leak-proof', 'Disinfection required']
    },
    '7': {
        'prefixes': ['Radioactive material', 'Uranium', 'Thorium', 'Plutonium', 'Cesium', 'Cobalt'],
        'suffixes': ['low specific activity', 'surface contaminated', 'Type A', 'Type B', 'Type C', 'fissile'],
        'uses': ['Medical', 'Industrial gauges', 'Research', 'Power generation', 'Imaging'],
        'provisions': ['Radiation hazard', 'Monitoring required', 'Shielding needed', 'Licensed transport']
    },
    '8': {
        'prefixes': ['Hydrochloric acid', 'Sulfuric acid', 'Nitric acid', 'Sodium hydroxide', 'Potassium hydroxide', 'Battery acid'],
        'suffixes': ['solution', 'spent', 'concentrated', 'diluted', 'mixture', 'corrosive'],
        'uses': ['Chemical production', 'Cleaning', 'Manufacturing', 'Water treatment', 'Battery'],
        'provisions': ['Corrosive', 'Severe burns', 'Eye protection', 'Avoid skin contact']
    },
    '9': {
        'prefixes': ['Lithium battery', 'Environmentally hazardous', 'Elevated temperature', 'Marine pollutant', 'Genetically modified'],
        'suffixes': ['liquid', 'solid', 'n.o.s.', 'miscellaneous', 'containing'],
        'uses': ['Electronics', 'Various industrial', 'Transport', 'Manufacturing', 'Research'],
        'provisions': ['Various hazards', 'Check SDS', 'Environmental protection', 'Special handling']
    }
}

# Flash points for Class 3
flashpoints = ['-60°C', '-43°C', '-30°C', '-20°C', '-10°C', '0°C', '13°C', '23°C', '38°C', '55°C', '60°C']

# Packing groups distribution
packing_groups = {
    '1.1': ['N/A'], '1.2': ['N/A'], '1.3': ['N/A'], '1.4': ['N/A'],
    '2.1': ['N/A'], '2.2': ['N/A'], '2.3': ['N/A'],
    '3': ['I', 'II', 'III'],
    '4.1': ['I', 'II', 'III'], '4.2': ['I', 'II', 'III'], '4.3': ['I', 'II', 'III'],
    '5.1': ['I', 'II', 'III'], '5.2': ['N/A'],
    '6.1': ['I', 'II', 'III'], '6.2': ['N/A'],
    '7': ['N/A'],
    '8': ['I', 'II', 'III'],
    '9': ['II', 'III', 'N/A']
}



# Generator Function

def generate_dangerous_goods(target_count=1000):
    goods_list = []
    un_number_start = 1000
    
    # Calculate how many entries per class
    classes = list(class_templates.keys())
    per_class = target_count // len(classes)
    
    
    for class_id in classes:
        template = class_templates[class_id]
        
        print(f"  Generating Class {class_id}... ", end='')
        
        for i in range(per_class):
            # Generate UN number
            un_number = f"UN{un_number_start + len(goods_list)}"
            
            # Generate proper shipping name
            prefix = random.choice(template['prefixes'])
            suffix = random.choice(template['suffixes'])
            
            # Sometimes just use prefix, sometimes combine
            if random.random() > 0.3:
                proper_name = f"{prefix}, {suffix}"
            else:
                proper_name = prefix
            
            # Add variation
            if random.random() > 0.7:
                proper_name += ", n.o.s."
            
            # Select packing group
            pg = random.choice(packing_groups[class_id])
            
            # Flash point (only for Class 3)
            if class_id == '3':
                flash_point = random.choice(flashpoints)
            elif class_id in ['2.1', '4.1', '4.2']:
                flash_point = random.choice(['-60°C', '-30°C', '-20°C', 'N/A'])
            else:
                flash_point = 'N/A'
            
            # Select provisions and uses
            provision = random.choice(template['provisions'])
            use = random.choice(template['uses'])
            
            # Add some variation to provisions
            extra_provisions = [
                'Keep away from foodstuffs',
                'Proper ventilation required',
                'Segregate as per IMDG Code',
                'Emergency equipment nearby',
                'Special training required',
                'Consult SDS for details'
            ]
            
            if random.random() > 0.6:
                provision += ' - ' + random.choice(extra_provisions)
            
            # Create entry
            entry = {
                'un_number': un_number,
                'proper_shipping_name': proper_name,
                'class_id': class_id,
                'packing_group': pg,
                'flash_point': flash_point,
                'special_provisions': provision,
                'common_uses': use
            }
            
            goods_list.append(entry)
        
        print(f"{len([g for g in goods_list if g['class_id'] == class_id])} entries")
    
    # Add some extra entries to reach target
    remaining = target_count - len(goods_list)
    if remaining > 0:
        print(f"\n➕ Adding {remaining} additional entries...")
        for i in range(remaining):
            class_id = random.choice(classes)
            template = class_templates[class_id]
            
            un_number = f"UN{un_number_start + len(goods_list)}"
            prefix = random.choice(template['prefixes'])
            suffix = random.choice(template['suffixes'])
            proper_name = f"{prefix}, {suffix}"
            
            entry = {
                'un_number': un_number,
                'proper_shipping_name': proper_name,
                'class_id': class_id,
                'packing_group': random.choice(packing_groups[class_id]),
                'flash_point': random.choice(flashpoints) if class_id == '3' else 'N/A',
                'special_provisions': random.choice(template['provisions']),
                'common_uses': random.choice(template['uses'])
            }
            goods_list.append(entry)
    
    return goods_list



if __name__ == "__main__":
  
    # Generate the data
    target_entries = 1200  # Generate more than 1000 for variety
    dangerous_goods = generate_dangerous_goods(target_entries)
    
    # Create DataFrame
    df = pd.DataFrame(dangerous_goods)
    
    # Shuffle to mix classes
    df = df.sample(frac=1).reset_index(drop=True)
    
    # Save to CSV
    
    
    
    if os.path.isfile("/data/sample_goods.csv"):
         print ("sample_goods.csv already exists")
    else:
        df.to_csv('data/sample_goods.csv', index=False)
        print("sample_goods.csv generated successfully")
        print(f"   • Total entries: {len(df)}")
        print(f"   • File size: {os.path.getsize('data/sample_goods.csv') / 1024:.2f} KB")
    
   

    

