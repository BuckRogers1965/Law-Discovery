# law_discovery.py (FINAL, SYNCHRONOUS INITIALIZATION VERSION)

# All your imports stay the same
import numpy as np
import sympy as sp
from typing import Dict, List, Tuple, Optional, Set, Union
from dataclasses import dataclass, field
from fractions import Fraction
from enum import Enum
import itertools
import json

# All your helper classes (UnitSystem, PhysicalQuantity) remain unchanged
class UnitSystem(Enum):
    SI = "SI"
    CGS = "CGS"
    PLANCK = "Planck"

@dataclass
class PhysicalQuantity:
    name: str
    symbol: str
    dimensions: Dict[str, int] = field(compare=False)
    typical_values: Dict[str, float] = field(default_factory=dict, compare=False)
    description: str = ""
    def __repr__(self):
        dim_str = " ".join([f"{dim}^{exp}" if exp != 1 else dim 
                           for dim, exp in self.dimensions.items() if exp != 0])
        return f"{self.symbol} [{dim_str or '1'}]"
    def __eq__(self, other):
        if not isinstance(other, PhysicalQuantity): return NotImplemented
        return self.name == other.name
    def __hash__(self):
        return hash(self.name)

class EnhancedPhysicsDisentangler:
    """
    This is the full, powerful engine, but modified with a synchronous
    initialize() method to match the interface contract of the working main.js.
    """
    
    # --- The Corrected Initialization Structure ---
    def __init__(self, unit_system: UnitSystem = UnitSystem.SI):
        """A lightweight constructor."""
        self.unit_system = unit_system
        self.quantities = {}
        self.derived_formulas = {}
        self.initialized = False
        print("Python: Real engine created. Call initialize() to build the library.")

    def initialize(self):
        """
        Builds the quantity library. THIS IS A SYNCHRONOUS,
        POTENTIALLY BLOCKING OPERATION. It is designed this way to match
        the existing main.js file.
        """
        print("Python: Real engine synchronous initialize() called...")
        if self.initialized:
            print("Python: Engine already initialized.")
            return

        # The heavy work happens here. This may cause a temporary freeze in the browser.
        self.quantities = self._build_quantity_library()
        self.initialized = True
        print(f"Python: Initialization complete. {len(self.quantities)} quantities loaded.")
    
    # --- The rest of the class is your original, powerful code ---
    
    def _build_quantity_library(self) -> Dict[str, PhysicalQuantity]:
        """Extended library of physical quantities (Unchanged)"""
        # This is the heavy part.
        base_quantities = {
            # Base quantities
            'dimensionless': PhysicalQuantity('dimensionless', 'D', {'L': 0, 'M': 0, 'T': 0, 'Θ':0}, description="dimensionless"),
            'length': PhysicalQuantity('length', 'L', {'L': 1}, description="Spatial dimension"),
            'mass': PhysicalQuantity('mass', 'm', {'M': 1}, description="Measure of matter"),
            'i_mass': PhysicalQuantity('mass', 'm_i', {'M': -1}, description="Inverse measure of matter"),
            'time': PhysicalQuantity('time', 't', {'T': 1}, description="Temporal dimension"),
            'temperature': PhysicalQuantity('temperature', 'T', {'Θ': 1}, description="Thermal energy scale"),
            'charge': PhysicalQuantity('charge', 'q', {'Q': 1}, description="Electric charge"),
            'amount': PhysicalQuantity('amount', 'n', {'N': 1}, description="Amount of substance"),
            'volume': PhysicalQuantity('volume', 'vol', {'L': 3}, description="Volume of substance"),
            'area': PhysicalQuantity('area', 'area', {'L': 2}, description="Area of substance"),
            'velocity': PhysicalQuantity('velocity', 'v', {'L': 1, 'T': -1}, description="Rate of position change"),
            'acceleration': PhysicalQuantity('acceleration', 'a', {'L': 1, 'T': -2}, description="Rate of velocity change"),
            'force': PhysicalQuantity('force', 'F', {'M': 1, 'L': 1, 'T': -2}, description="Interaction causing acceleration"),
            'energy': PhysicalQuantity('energy', 'E', {'M': 1, 'L': 2, 'T': -2}, description="Capacity to do work"),
            'power': PhysicalQuantity('power', 'P', {'M': 1, 'L': 2, 'T': -3}, description="Rate of energy transfer"),
            'pressure': PhysicalQuantity('pressure', 'Pres', {'M': 1, 'L': -1, 'T': -2}, description="Pressure"),
            'density': PhysicalQuantity('density', 'rho', {'M': 1, 'L': -3}, description="Density"),
            'momentum': PhysicalQuantity('momentum', 'p', {'M': 1, 'L': 1, 'T': -1}, description="Mass times velocity"),
            'angular_momentum': PhysicalQuantity('angular_momentum', 'L_ang', {'M': 1, 'L': 2, 'T': -1}, description="Rotational momentum"),
            'e-tensor': PhysicalQuantity('E-tensor', 'et', {'L': -2}, description="Einstein tensor"),
            'se-tensor': PhysicalQuantity('set', 'set', {'M': 1, 'L': -1, 'T': -2}, description="Stress-energy tensor"),
            'frequency': PhysicalQuantity('frequency', 'f', {'T': -1}, description="Oscillations per unit time"),
            'wavelength': PhysicalQuantity('wavelength', 'λ', {'L': 1}, description="Spatial period of wave"),
            'wavenumber': PhysicalQuantity('wavenumber', 'k', {'L': -1}, description="Spatial frequency"),
            'action': PhysicalQuantity('action', 'S', {'M': 1, 'L': 2, 'T': -1}, description="Energy-time integral"),
            'entropy': PhysicalQuantity('entropy', 'S_ent', {'M': 1, 'L': 2, 'T': -2, 'Θ': -1}, description="Measure of disorder"),
            'heat_capacity': PhysicalQuantity('heat_capacity', 'C', {'M': 1, 'L': 2, 'T': -2, 'Θ': -1}, description="Heat required per temperature change"),
            'electric_field': PhysicalQuantity('electric_field', 'E_field', {'M': 1, 'L': 1, 'T': -3, 'Q': -1}, description="Force per unit charge"),
            'magnetic_field': PhysicalQuantity('magnetic_field', 'B', {'M': 1, 'T': -2, 'Q': -1}, description="Magnetic flux density"),
            'voltage': PhysicalQuantity('voltage', 'V', {'M': 1, 'L': 2, 'T': -3, 'Q': -1}, description="Electric potential difference"),
            'current': PhysicalQuantity('current', 'I', {'Q': 1, 'T': -1}, description="Rate of charge flow"),
            'resistance': PhysicalQuantity('resistance', 'R_elec', {'M': 1, 'L': 2, 'T': -3, 'Q': -2}, description="Opposition to current flow"),
            'capacitance': PhysicalQuantity('capacitance', 'C_cap', {'M': -1, 'L': -2, 'T': 4, 'Q': 2}, description="Charge storage capacity"),
            'planck_constant': PhysicalQuantity('planck_constant', 'h', {'M': 1, 'L': 2, 'T': -1}, description="Quantum of action"),
            'reduced_planck': PhysicalQuantity('reduced_planck', 'ℏ', {'M': 1, 'L': 2, 'T': -1}, description="h/2π"),
            'boltzmann_constant': PhysicalQuantity('boltzmann_constant', 'k_B', {'M': 1, 'L': 2, 'T': -2, 'Θ': -1}, description="Thermal energy scale"),
            'speed_of_light': PhysicalQuantity('speed_of_light', 'c', {'L': 1, 'T': -1}, description="Universal speed limit"),
            'speed_of_light_cubed': PhysicalQuantity('speed_of_light_cubed', 'c^3', {'L': 3, 'T': -3}, description="Universal speed limit cubed"),
            'gravitational_constant': PhysicalQuantity('gravitational_constant', 'G', {'M': -1, 'L': 3, 'T': -2}, description="Gravity coupling constant"),
            'gas_constant': PhysicalQuantity('gas_constant', 'R_gas', {'M': 1, 'L': 2, 'T': -2, 'Θ': -1, 'N': -1}, description="Universal gas constant"),
            'avogadro_number': PhysicalQuantity('avogadro_number', 'N_A', {'N': -1}, description="Particles per mole"),
            'elementary_charge': PhysicalQuantity('elementary_charge', 'e', {'Q': 1}, description="Fundamental charge unit"),
            'vacuum_permittivity': PhysicalQuantity('vacuum_permittivity', 'ε₀', {'M': -1, 'L': -3, 'T': 4, 'Q': 2}, description="Electric constant"),
            'vacuum_permeability': PhysicalQuantity('vacuum_permeability', 'μ₀', {'M': 1, 'L': 1, 'T': -2, 'Q': -2}, description="Magnetic constant"),
            'fine_structure': PhysicalQuantity('fine_structure', 'α', {}, description="Electromagnetic coupling constant"),
            'electron_mass': PhysicalQuantity('electron_mass', 'm_e', {'M': 1}, description="Mass of electron"),
            'proton_mass': PhysicalQuantity('proton_mass', 'm_p', {'M': 1}, description="Mass of proton"),
        }
        return base_quantities

    def discover_relationship(self, output_quantity: str, input_quantities: List[str], constants_to_include: Optional[List[str]] = None, auto_search: bool = False, verbose: bool = False) -> Dict:
        """Main discovery engine."""
        
        # --- THIS IS THE FIX ---
        # Explicitly convert the incoming JavaScript Proxies to Python lists.
        # The .to_py() method does this conversion.
        input_quantities = input_quantities.to_py()
        constants_to_include = constants_to_include.to_py()
        # --- END OF THE FIX ---

        if not self.initialized:
            return {'success': False, 'message': 'FATAL ERROR: Engine not initialized. The initialize() method must be called first.'}
        
        try:
            all_qs_names = [output_quantity] + input_quantities + (constants_to_include or [])
            seen = set()
            unique_qs = [self.quantities[name] for name in all_qs_names if name not in seen and not seen.add(name)]
        except KeyError as e:
            return {'success': False, 'message': f"Unknown quantity: '{e}'. Please check the list of available quantities."}
            
        dimensions = self.get_all_dimensions(unique_qs)
        if not dimensions and len(unique_qs) > 1:
             return { 'success': True, 'formula': f"{unique_qs[0].symbol} = Π × {'×'.join(q.symbol for q in unique_qs[1:])}", 'message': "Relationship between dimensionless quantities." }

        status, exponents, message = self.solve_and_diagnose(unique_qs, dimensions)
        
        if status == 'SUCCESS':
            formula = self.format_formula(unique_qs, exponents)
            validation = self.validate_physical_reasonableness(formula, unique_qs, exponents)
            return { 'success': True, 'formula': formula, 'validation': validation, 'message': message }

        if auto_search and status in ['FAIL_INCONSISTENT', 'FAIL_UNDERDETERMINED']:
            # ... (the rest of your auto-search logic is unchanged)
            suggestions = []
            if status == 'FAIL_UNDERDETERMINED':
                suggestions = self._get_suggestions(unique_qs, missing_dims=None)
            else: 
                input_dim_names = {dim for q in unique_qs[1:] for dim in q.dimensions}
                missing_dims_dict = { dim: power for dim, power in unique_qs[0].dimensions.items() if power != 0 and dim not in input_dim_names }
                suggestions = self._get_suggestions(unique_qs, missing_dims=missing_dims_dict if missing_dims_dict else None)
            
            search_log = ["Auto-search initiated..."]
            for suggestion in suggestions:
                if suggestion in {q.name for q in unique_qs}: continue
                
                search_log.append(f"   ► Trying to add '{suggestion}'...")
                
                new_constants = (constants_to_include or []) + [suggestion]
                recursive_result = self.discover_relationship(output_quantity, input_quantities, new_constants, auto_search=True, verbose=False)
                
                if recursive_result.get('success'):
                    recursive_result['message'] = f"Auto-search found a solution by adding '{suggestion}'."
                    return recursive_result
            
            # If the loop finishes, append the log to the original failure message
            final_message = message + "\n\n--- Auto-Search Log ---\n" + "\n".join(search_log)
            return {'success': False, 'message': final_message}

        return {'success': False, 'message': message}

    # All your other helper methods (`_get_suggestions`, `solve_and_diagnose`, etc.) are unchanged.
    # Just paste them in here.
    def get_all_dimensions(self, quantities: List[PhysicalQuantity]) -> List[str]:
        all_dims = set()
        for q in quantities: all_dims.update(q.dimensions.keys())
        return sorted(list(all_dims))

    def build_dimensional_matrix(self, quantities: List[PhysicalQuantity], dimensions: List[str]) -> np.ndarray:
        return np.array([[q.dimensions.get(dim, 0) for q in quantities] for dim in dimensions], dtype=float)

    def solve_and_diagnose(self, quantities: List[PhysicalQuantity], dimensions: List[str]) -> Tuple[str, Optional[np.ndarray], str]:
        if len(quantities) < 2: return 'FAIL_INSUFFICIENT_VARS', None, "Hypothesis requires at least 2 quantities."
        input_dim_names = {dim for q in quantities[1:] for dim in q.dimensions}
        missing_dims_dict = {dim: power for dim, power in quantities[0].dimensions.items() if power != 0 and dim not in input_dim_names}
        if missing_dims_dict:
            suggestions = self._get_suggestions(quantities, missing_dims=missing_dims_dict)
            superscript_map = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
            missing_dims_formatted = [f"{dim}{str(power).translate(superscript_map)}" if power != 1 else dim for dim, power in sorted(missing_dims_dict.items())]
            return 'FAIL_INCONSISTENT', None, f"Hypothesis is impossible. Inputs are missing required dimensions.\n       Reason: Output requires '{', '.join(missing_dims_formatted)}', not present in inputs.\n       Suggestion: Try adding: {', '.join(suggestions)}"
        dim_matrix = self.build_dimensional_matrix(quantities, dimensions)
        A = sp.Matrix(dim_matrix[:, 1:])
        b = sp.Matrix(-dim_matrix[:, 0])
        num_inputs, rank_A = A.cols, A.rank()
        if rank_A < A.row_join(b).rank():
            rref_aug, _ = A.row_join(b).rref()
            failing_dim = "an unknown dimension"
            for row in range(rref_aug.rows):
                if all(rref_aug[row, col] == 0 for col in range(num_inputs)) and rref_aug[row, -1] != 0:
                    failing_dim = dimensions[row]; break
            suggestions = self._get_suggestions(quantities, missing_dims=None)
            return 'FAIL_INCONSISTENT', None, f"Hypothesis is dimensionally inconsistent.\n       Reason: The equation for '{failing_dim}' cannot be satisfied.\n       Analysis: The quantities have conflicting relationships.\n       Suggestion: A fundamental constant is likely needed. Try: {', '.join(suggestions)}"
        elif rank_A < num_inputs:
            suggestions = self._get_suggestions(quantities, missing_dims=None)
            return 'FAIL_UNDERDETERMINED', None, f"Hypothesis is underdetermined. Infinite solutions exist.\n       Reason: {num_inputs - rank_A + 1} dimensionless groups can be formed.\n       Suggestion: Add constants to constrain the system, such as: {', '.join(suggestions)}"
        else:
            solution_vector = A.LUsolve(b)
            return 'SUCCESS', np.concatenate([[1.0], -np.array(solution_vector, dtype=float).flatten()]), "Unique dimensionless relationship found."
    
    def _get_suggestions(self, quantities: List[PhysicalQuantity], missing_dims: Optional[Dict[str, int]] = None) -> List[str]:
        current_quantity_names = {q.name for q in quantities}
        if missing_dims:
            suggestions = []
            missing_dim_keys = set(missing_dims.keys())
            for name, quantity in self.quantities.items():
                if name in current_quantity_names: continue
                q_dims, score = quantity.dimensions, 0.0
                q_dim_keys = set(q_dims.keys())
                if q_dim_keys == missing_dim_keys: score += 10.0 if q_dims == missing_dims else 5.0
                else:
                    if not any(dim in q_dims for dim in missing_dim_keys): continue
                    score += sum(1.0 for dim in missing_dim_keys if dim in q_dims)
                    score -= len(q_dim_keys - missing_dim_keys) * 0.5
                if name in ['speed_of_light', 'planck_constant', 'gravitational_constant', 'boltzmann_constant']: score += 0.2
                if score > 0: suggestions.append((name, score))
            suggestions.sort(key=lambda x: x[1], reverse=True)
            return [name for name, score in suggestions[:4]]
        else:
            possible_additions = ['speed_of_light', 'planck_constant', 'gravitational_constant', 'boltzmann_constant', 'elementary_charge']
            return [p for p in possible_additions if p not in current_quantity_names]

    def format_formula(self, quantities: List[PhysicalQuantity], exponents: np.ndarray, include_units: bool = False) -> str:
        target_var = quantities[0].symbol
        numerator_terms, denominator_terms = [], []
        for i in range(1, len(quantities)):
            quantity, exp_val = quantities[i], exponents[i]
            if abs(exp_val) < 1e-10: continue
            exp_frac = Fraction(exp_val).limit_denominator(100)
            abs_exp_frac = abs(exp_frac)
            if abs_exp_frac.denominator == 2: term = f"√{quantity.symbol}" if abs_exp_frac.numerator == 1 else f"√({quantity.symbol}^{abs_exp_frac.numerator})"
            elif abs_exp_frac.denominator == 3: term = f"∛{quantity.symbol}" if abs_exp_frac.numerator == 1 else f"∛({quantity.symbol}^{abs_exp_frac.numerator})"
            elif abs_exp_frac.denominator == 1: term = quantity.symbol if abs_exp_frac.numerator == 1 else f"{quantity.symbol}^{abs_exp_frac.numerator}"
            else: term = f"{quantity.symbol}^{abs_exp_frac}"
            (numerator_terms if exp_frac > 0 else denominator_terms).append(term)
        if not numerator_terms and not denominator_terms: return f"{target_var} = Π"
        formula = f"{target_var} = Π"
        if numerator_terms or denominator_terms: formula += " × "
        if denominator_terms:
            num_str = "×".join(numerator_terms) if numerator_terms else "1"
            den_str = "×".join(denominator_terms)
            formula += f"{num_str}/{den_str}" if len(denominator_terms) == 1 else f"{num_str}/({den_str})"
        else: formula += "×".join(numerator_terms)
        return formula


# This block is for command-line use ONLY and will not run in the browser.
if __name__ == "__main__":
    engine = EnhancedPhysicsDisentangler()
    print("Initializing engine for command-line use...")
    engine.initialize()
    print("Engine ready.\n")
    # You would put your interactive_discovery() call here if you want it for command line
    # engine.interactive_discovery()
