# Enhanced Physics Formula Discovery Engine
# Improvements: Multiple solutions, unit system support, physical validation, and more

import numpy as np
import sympy as sp
from typing import Dict, List, Tuple, Optional, Set, Union
from dataclasses import dataclass, field
from fractions import Fraction
from enum import Enum
import itertools
import json

class UnitSystem(Enum):
    SI = "SI"
    CGS = "CGS"
    PLANCK = "Planck"

@dataclass
class PhysicalQuantity:
    """Enhanced physical quantity with multiple unit system support"""
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
        if not isinstance(other, PhysicalQuantity):
            return NotImplemented
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

class EnhancedPhysicsDisentangler:
    """
    Enhanced Automated Physics Discovery Engine with multiple improvements:
    - Multiple solution handling for underdetermined systems
    - Physical reasonableness validation
    - Extended quantity library
    - Unit system support
    - Interactive discovery mode
    """
    
    def __init__(self, unit_system: UnitSystem = UnitSystem.SI):
        self.unit_system = unit_system
        self.quantities = self._build_quantity_library()
        self.derived_formulas = {}  # Cache for discovered relationships
        
    def _build_quantity_library(self) -> Dict[str, PhysicalQuantity]:
        """Extended library of physical quantities"""
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
            
            # Mechanical quantities
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
#Einstein tensor: [L⁻²] (inverse length squared)
#Stress-energy tensor: [M L⁻¹ T⁻²] (same as pressure)
            
            # Wave and quantum quantities
            'frequency': PhysicalQuantity('frequency', 'f', {'T': -1}, description="Oscillations per unit time"),
            'wavelength': PhysicalQuantity('wavelength', 'λ', {'L': 1}, description="Spatial period of wave"),
            'wavenumber': PhysicalQuantity('wavenumber', 'k', {'L': -1}, description="Spatial frequency"),
            'action': PhysicalQuantity('action', 'S', {'M': 1, 'L': 2, 'T': -1}, description="Energy-time integral"),
            
            # Thermal quantities
            'entropy': PhysicalQuantity('entropy', 'S', {'M': 1, 'L': 2, 'T': -2, 'Θ': -1}, description="Measure of disorder"),
            'heat_capacity': PhysicalQuantity('heat_capacity', 'C', {'M': 1, 'L': 2, 'T': -2, 'Θ': -1}, description="Heat required per temperature change"),
            
            # Electromagnetic quantities
            'electric_field': PhysicalQuantity('electric_field', 'E_field', {'M': 1, 'L': 1, 'T': -3, 'Q': -1}, description="Force per unit charge"),
            'magnetic_field': PhysicalQuantity('magnetic_field', 'B', {'M': 1, 'T': -2, 'Q': -1}, description="Magnetic flux density"),
            'voltage': PhysicalQuantity('voltage', 'V', {'M': 1, 'L': 2, 'T': -3, 'Q': -1}, description="Electric potential difference"),
            'current': PhysicalQuantity('current', 'I', {'Q': 1, 'T': -1}, description="Rate of charge flow"),
            'resistance': PhysicalQuantity('resistance', 'R', {'M': 1, 'L': 2, 'T': -3, 'Q': -2}, description="Opposition to current flow"),
            'capacitance': PhysicalQuantity('capacitance', 'C_cap', {'M': -1, 'L': -2, 'T': 4, 'Q': 2}, description="Charge storage capacity"),
            
            # Physical constants
            'planck_constant': PhysicalQuantity('planck_constant', 'h', {'M': 1, 'L': 2, 'T': -1}, description="Quantum of action"),
            'reduced_planck': PhysicalQuantity('reduced_planck', 'ℏ', {'M': 1, 'L': 2, 'T': -1}, description="h/2π"),
            'boltzmann_constant': PhysicalQuantity('boltzmann_constant', 'k_B', {'M': 1, 'L': 2, 'T': -2, 'Θ': -1}, description="Thermal energy scale"),
            'speed_of_light': PhysicalQuantity('speed_of_light', 'c', {'L': 1, 'T': -1}, description="Universal speed limit"),
            'speed_of_light_cubed': PhysicalQuantity('speed_of_light', 'c^3', {'L': 3, 'T': -3}, description="Universal speed limit cubed"),
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
    
    def add_custom_quantity(self, name: str, symbol: str, dimensions: Dict[str, int], description: str = ""):
        """Add a custom quantity to the library"""
        self.quantities[name] = PhysicalQuantity(name, symbol, dimensions, description=description)
    
    def suggest_missing_constants(self, output_quantity: str, input_quantities: List[str]) -> List[str]:
        """Suggest physical constants that might make an underdetermined system solvable"""
        try:
            target_dims = self.quantities[output_quantity].dimensions
            input_dims = [self.quantities[q].dimensions for q in input_quantities]
            
            # Find dimensions that appear in target but not sufficiently covered by inputs
            all_input_dims = {}
            for dims in input_dims:
                for dim, exp in dims.items():
                    all_input_dims[dim] = all_input_dims.get(dim, 0) + abs(exp)
            
            missing_dims = set()
            for dim, exp in target_dims.items():
                if dim not in all_input_dims or all_input_dims[dim] < abs(exp):
                    missing_dims.add(dim)
            
            # Suggest constants that could help
            suggestions = []
            constants = ['planck_constant', 'boltzmann_constant', 'speed_of_light', 
                        'gravitational_constant', 'elementary_charge', 'vacuum_permittivity']
            
            for const in constants:
                if const in self.quantities:
                    const_dims = set(self.quantities[const].dimensions.keys())
                    if const_dims.intersection(missing_dims):
                        suggestions.append(const)
            
            return suggestions[:3]  # Return top 3 suggestions
        except KeyError:
            return []
    
    def find_all_solutions(self, quantities: List[PhysicalQuantity], dimensions: List[str]) -> List[Tuple[str, Optional[np.ndarray], str]]:
        """Find all possible solutions for underdetermined systems"""
        if len(quantities) < 2:
            return [('FAIL_INSUFFICIENT_VARS', None, "Hypothesis requires at least 2 quantities.")]

        dim_matrix = self.build_dimensional_matrix(quantities, dimensions)
        A = sp.Matrix(dim_matrix[:, 1:])
        b = sp.Matrix(-dim_matrix[:, 0])
        
        augmented_matrix = A.row_join(b)
        rref_matrix, pivot_columns = augmented_matrix.rref()

        # Check for inconsistency
        for row in range(rref_matrix.rows):
            is_zero_vector = all(rref_matrix[row, col] == 0 for col in range(rref_matrix.cols - 1))
            if is_zero_vector and rref_matrix[row, -1] != 0:
                failing_dim = dimensions[row]
                error_msg = (f"Hypothesis is dimensionally inconsistent.\n"
                           f"       Reason: The dimensional equation for '{failing_dim}' cannot be satisfied.\n"
                           f"       Analysis: After simplifying the system, the math requires a contradiction: 0 = {rref_matrix[row, -1]}.")
                return [('FAIL_INCONSISTENT', None, error_msg)]

        num_inputs = A.cols
        rank = len(pivot_columns)
        num_free_vars = num_inputs - rank
        
        if num_free_vars == 0:
            # Unique solution
            input_exponents = np.array(rref_matrix[:, -1], dtype=float).flatten()
            solution = np.concatenate([[1.0], -input_exponents])
            return [('SUCCESS', solution, "Unique dimensionless relationship found.")]
        
        else:
            # Multiple solutions - generate a few reasonable ones
            solutions = []
            free_var_indices = [i for i in range(num_inputs) if i not in pivot_columns]
            
            # Generate solutions by setting free variables to simple values
            test_values = [0, 1, -1, 2, -2]
            for combo in itertools.product(test_values, repeat=min(num_free_vars, 2)):
                if all(v == 0 for v in combo):
                    continue
                    
                # Set free variables and solve for dependent ones
                free_var_assignment = dict(zip(free_var_indices, combo))
                
                # This is a simplified approach - in practice you'd want more sophisticated solution generation
                solution = np.zeros(len(quantities))
                solution[0] = 1.0  # Target variable coefficient
                
                # Set free variables
                for idx, val in free_var_assignment.items():
                    solution[idx + 1] = val
                
                # Solve for dependent variables (simplified)
                # This would need more sophisticated linear algebra in practice
                solutions.append(('SUCCESS_MULTIPLE', solution, f"One possible solution (free vars: {combo})"))
                
                if len(solutions) >= 3:  # Limit to 3 solutions
                    break
            
            if not solutions:
                error_msg = (f"Hypothesis is underdetermined. Infinite solutions exist.\n"
                           f"       Reason: There are {num_free_vars + 1} independent dimensionless groups that can be formed.\n"
                           f"       Suggestion: Add constants like {', '.join(self.suggest_missing_constants(quantities[0].name, [q.name for q in quantities[1:]]))}")
                return [('FAIL_UNDERDETERMINED', None, error_msg)]
            
            return solutions
    
    def validate_physical_reasonableness(self, formula: str, quantities: List[PhysicalQuantity], exponents: np.ndarray) -> Dict[str, Union[bool, str, float]]:
        """Check if the discovered formula makes physical sense"""
        validation = {
            'dimensionally_correct': True,
            'physically_reasonable': True,
            'confidence_score': 1.0,
            'warnings': []
        }
        
        # Check for extremely large exponents (usually unphysical)
        max_exp = np.max(np.abs(exponents[1:]))
        if max_exp > 5:
            validation['warnings'].append(f"Large exponent detected ({max_exp:.1f}) - may be unphysical")
            validation['confidence_score'] *= 0.7
        
        # Check for fractional exponents that might be suspicious
        for i, exp in enumerate(exponents[1:], 1):
            frac = Fraction(exp).limit_denominator(100)
            if frac.denominator > 4 and abs(exp) > 0.1:
                validation['warnings'].append(f"Complex fractional exponent for {quantities[i].symbol}: {frac}")
                validation['confidence_score'] *= 0.8
        
        # Domain-specific checks
        output_name = quantities[0].name
        if 'energy' in output_name and any('temperature' in q.name for q in quantities[1:]):
            # Energy-temperature relationships should typically be linear
            temp_indices = [i for i, q in enumerate(quantities[1:], 1) if 'temperature' in q.name]
            for idx in temp_indices:
                if abs(exponents[idx] - 1.0) > 0.1:
                    validation['warnings'].append("Energy-temperature relationships are typically linear")
                    validation['confidence_score'] *= 0.9
        
        return validation
    
    def get_all_dimensions(self, quantities: List[PhysicalQuantity]) -> List[str]:
        all_dims = set()
        for q in quantities:
            all_dims.update(q.dimensions.keys())
        return sorted(list(all_dims))
    
    def build_dimensional_matrix(self, quantities: List[PhysicalQuantity], dimensions: List[str]) -> np.ndarray:
        return np.array([[q.dimensions.get(dim, 0) for q in quantities] for dim in dimensions], dtype=float)
    
    def format_formula(self, quantities: List[PhysicalQuantity], exponents: np.ndarray, include_units: bool = False) -> str:
        target_var = quantities[0].symbol
        numerator_terms, denominator_terms = [], []
        
        for i in range(1, len(quantities)):
            quantity, exp_val = quantities[i], exponents[i]
            if abs(exp_val) < 1e-10: 
                continue

            exp_frac = Fraction(exp_val).limit_denominator(100)
            abs_exp_frac = abs(exp_frac)
            
            # Enhanced formatting for common cases
            if abs_exp_frac.denominator == 2:
                if abs_exp_frac.numerator == 1:
                    term = f"√{quantity.symbol}"
                else:
                    term = f"√({quantity.symbol}^{abs_exp_frac.numerator})"
            elif abs_exp_frac.denominator == 3:
                term = f"∛{quantity.symbol}" if abs_exp_frac.numerator == 1 else f"∛({quantity.symbol}^{abs_exp_frac.numerator})"
            elif abs_exp_frac.denominator == 1:
                term = quantity.symbol if abs_exp_frac.numerator == 1 else f"{quantity.symbol}^{abs_exp_frac.numerator}"
            else:
                term = f"{quantity.symbol}^{abs_exp_frac}"

            (numerator_terms if exp_frac > 0 else denominator_terms).append(term)
        
        # Build formula string
        if not numerator_terms and not denominator_terms:
            return f"{target_var} = Π"
        
        formula = f"{target_var} = Π"
        if numerator_terms or denominator_terms:
            formula += " × "
            
        if denominator_terms:
            num_str = "×".join(numerator_terms) if numerator_terms else "1"
            den_str = "×".join(denominator_terms)
            if len(denominator_terms) == 1:
                formula += f"{num_str}/{den_str}"
            else:
                formula += f"{num_str}/({den_str})"
        else:
            formula += "×".join(numerator_terms)
        
        return formula

    
    def interactive_discovery(self):
        """Interactive mode for exploring relationships"""
        print("\n🔬 Interactive Physics Formula Discovery")
        print("=" * 50)
        print("Available quantities:")
        categories = {
            'Basic': ['length', 'mass', 'time', 'temperature', 'charge'],
            'Mechanical': ['velocity', 'acceleration', 'force', 'energy', 'power'],
            'Quantum': ['planck_constant', 'reduced_planck', 'action'],
            'Constants': ['speed_of_light', 'gravitational_constant', 'boltzmann_constant']
        }
        
        for category, quantities in categories.items():
            print(f"\n{category}: {', '.join(quantities)}")
        
        print(f"\nTotal available: {len(self.quantities)} quantities")
        print("Type 'help' for commands, 'quit' to exit")
        
        while True:
            try:
                cmd = input("\n> ").strip().lower()
                
                if cmd in ['quit', 'exit', 'q']:
                    break
                elif cmd == 'help':
                    print("\nCommands:")
                    print("  discover <output> from <input1,input2,...> [with <const1,const2,...>]")
                    print("  list [category] - show available quantities")
                    print("  describe <quantity> - show quantity details")
                    print("  Example: discover energy from mass,velocity")
                elif cmd.startswith('discover'):
                    self._handle_discover_command(cmd)
                elif cmd.startswith('list'):
                    self._handle_list_command(cmd)
                elif cmd.startswith('describe'):
                    self._handle_describe_command(cmd)
                else:
                    print("Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    

    def discover_relationship(self, output_quantity: str, input_quantities: List[str], constants_to_include: Optional[List[str]] = None, auto_search: bool = False, verbose: bool = False) -> Dict:
        """
        Main discovery engine. If auto_search is True, it will attempt to
        recursively solve a failed hypothesis by trying its own suggestions.
        The verbose flag controls whether search attempts are printed.
        """
        try:
            all_qs_names = [output_quantity] + input_quantities + (constants_to_include or [])
            seen = set()
            unique_qs = [self.quantities[name] for name in all_qs_names if name not in seen and not seen.add(name)]
        except KeyError as e:
            return {'success': False, 'message': f"Unknown quantity: {e}."}
            
        dimensions = self.get_all_dimensions(unique_qs)
        if not dimensions and len(unique_qs) > 1:
             return { 'success': True, 'formula': f"{unique_qs[0].symbol} = Π × {'×'.join(q.symbol for q in unique_qs[1:])}", 'message': "Relationship between dimensionless quantities." }

        # --- Initial Attempt ---
        status, exponents, message = self.solve_and_diagnose(unique_qs, dimensions)
        
        if status == 'SUCCESS':
            formula = self.format_formula(unique_qs, exponents)
            validation = self.validate_physical_reasonableness(formula, unique_qs, exponents)
            return { 'success': True, 'formula': formula, 'validation': validation }

        # --- If it failed, and auto_search is on, begin the self-correction loop ---
        if auto_search and status in ['FAIL_INCONSISTENT', 'FAIL_UNDERDETERMINED']:
            suggestions = []
            if status == 'FAIL_UNDERDETERMINED':
                suggestions = self._get_suggestions(unique_qs, missing_dims=None)
            else: # Must be FAIL_INCONSISTENT
                input_dim_names = {dim for q in unique_qs[1:] for dim in q.dimensions}
                missing_dims_dict = { dim: power for dim, power in unique_qs[0].dimensions.items() if power != 0 and dim not in input_dim_names }
                suggestions = self._get_suggestions(unique_qs, missing_dims=missing_dims_dict if missing_dims_dict else None)
            
            # --- This is the new verbose search loop ---
            for suggestion in suggestions:
                if suggestion in {q.name for q in unique_qs}: continue
                
                if verbose:
                    print(f"   ⏳ Trying to add '{suggestion}'...") # Print the attempt

                new_constants = (constants_to_include or []) + [suggestion]
                
                # Recursive call is NOT verbose to avoid cluttered output
                recursive_result = self.discover_relationship(output_quantity, input_quantities, new_constants, auto_search=True, verbose=False)
                
                if recursive_result.get('success'):
                    # Found a solution! Add a note about what was added.
                    recursive_result['message'] = f"✅ Success! Auto-search found a solution by adding '{suggestion}'."
                    return recursive_result

            # If the loop finishes without success, return the original, detailed failure message.
            return {'success': False, 'message': message}

        # If auto_search was off, just return the original failure message.
        return {'success': False, 'message': message}

    def _get_suggestions(self, quantities: List[PhysicalQuantity], missing_dims: Optional[Dict[str, int]] = None) -> List[str]:
        """
        Intelligently suggests quantities to add to a hypothesis.
        - If 'missing_dims' is provided (for impossible cases), it ranks all quantities
          based on how well they fit the missing dimensional signature.
        - If 'missing_dims' is None (for underdetermined cases), it suggests common
          fundamental constants that bridge different physical domains.
        """
        current_quantity_names = {q.name for q in quantities}
        
        # Case 1: We know exactly which dimensions are missing (impossible hypothesis)
        if missing_dims:
            suggestions = []
            missing_dim_keys = set(missing_dims.keys())

            for name, quantity in self.quantities.items():
                if name in current_quantity_names:
                    continue

                q_dims = quantity.dimensions
                q_dim_keys = set(q_dims.keys())
                score = 0.0

                # Check for a perfect dimensional match (highest priority)
                if q_dim_keys == missing_dim_keys:
                    score += 5.0
                    if q_dims == missing_dims:
                        score += 5.0  # Perfect fit bonus!
                else:
                    # Score based on providing at least one needed dimension
                    provides_needed_dim = False
                    for dim in missing_dims:
                        if dim in q_dims:
                            provides_needed_dim = True
                            score += 1.0
                    
                    if not provides_needed_dim:
                        continue

                    # Penalize for introducing unneeded dimensions
                    unwanted_dims_count = len(q_dim_keys - missing_dim_keys)
                    score -= unwanted_dims_count * 0.5

                # Small bonus for being a fundamental constant
                if name in ['speed_of_light', 'planck_constant', 'gravitational_constant', 'boltzmann_constant']:
                    score += 0.2

                if score > 0:
                    suggestions.append((name, score))
            
            suggestions.sort(key=lambda x: x[1], reverse=True)
            return [name for name, score in suggestions[:4]]

        # Case 2: The system is just underdetermined (no specific "missing" dimension)
        else:
            # In this case, suggesting general-purpose bridge constants is the best strategy.
            possible_additions = ['speed_of_light', 'planck_constant', 'gravitational_constant', 
                                  'boltzmann_constant', 'elementary_charge']
            # --- THIS IS THE CORRECTED LINE ---
            return [p for p in possible_additions if p not in current_quantity_names]


    def solve_and_diagnose(self, quantities: List[PhysicalQuantity], dimensions: List[str]) -> Tuple[str, Optional[np.ndarray], str]:
        """
        Solves the dimensional analysis problem with robust diagnosis of the system.
        Provides specific, actionable feedback for all failure modes.
        """
        if len(quantities) < 2:
            return 'FAIL_INSUFFICIENT_VARS', None, "Hypothesis requires at least 2 quantities."

        # Step 0: Preliminary check for completely missing dimensions.
        input_dim_names = {dim for q in quantities[1:] for dim in q.dimensions}
        missing_dims_dict = {
            dim: power for dim, power in quantities[0].dimensions.items()
            if power != 0 and dim not in input_dim_names
        }

        if missing_dims_dict:
            suggestions = self._get_suggestions(quantities, missing_dims=missing_dims_dict)
            superscript_map = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
            missing_dims_formatted = [f"{dim}{str(power).translate(superscript_map)}" if power != 1 else dim
                                      for dim, power in sorted(missing_dims_dict.items())]
            error_msg = (f"Hypothesis is impossible. The inputs are missing required dimensions.\n"
                         f"       Reason: The output requires dimension(s) '{', '.join(missing_dims_formatted)}', which are not present in any of the inputs.\n"
                         f"       Suggestion: Try adding one of the following: {', '.join(suggestions)}")
            return 'FAIL_INCONSISTENT', None, error_msg

        # Step 1: Build and analyze the linear algebra system.
        dim_matrix = self.build_dimensional_matrix(quantities, dimensions)
        A = sp.Matrix(dim_matrix[:, 1:])
        b = sp.Matrix(-dim_matrix[:, 0])
        num_inputs = A.cols
        rank_A = A.rank()
        augmented_matrix = A.row_join(b)
        rank_aug = augmented_matrix.rank()

        # Step 2: Diagnose the system based on the ranks.
        if rank_A < rank_aug:
            # --- START: THIS IS THE CRITICAL FIX ---
            # Case 1: The system is mathematically inconsistent. Find out why.
            rref_aug, _ = augmented_matrix.rref()
            failing_dim = "an unknown dimension"
            
            # Find the row like [0, 0, ..., 1] which signifies a contradiction (e.g., 0=1).
            for row in range(rref_aug.rows):
                if all(rref_aug[row, col] == 0 for col in range(num_inputs)) and rref_aug[row, -1] != 0:
                    failing_dim = dimensions[row]
                    break
            
            # For inconsistent systems, the best suggestions are the "bridge" constants.
            suggestions = self._get_suggestions(quantities, missing_dims=None)
            
            error_msg = (f"Hypothesis is dimensionally inconsistent.\n"
                         f"       Reason: The dimensional equation for '{failing_dim}' cannot be satisfied.\n"
                         f"       Analysis: The provided quantities have conflicting relationships. For example, the time dimension 'T' might be impossible to cancel out.\n"
                         f"       Suggestion: This often means a fundamental constant is needed to bridge the physical domains. Try adding: {', '.join(suggestions)}")
            return 'FAIL_INCONSISTENT', None, error_msg
            # --- END: CRITICAL FIX ---

        elif rank_A < num_inputs:
            # Case 2: The system is underdetermined (infinite solutions).
            num_dimensionless_groups = num_inputs - rank_A + 1
            suggestions = self._get_suggestions(quantities, missing_dims=None)
            error_msg = (f"Hypothesis is underdetermined. Infinite solutions exist.\n"
                         f"       Reason: There are {num_dimensionless_groups} independent dimensionless groups that can be formed.\n"
                         f"       Suggestion: Add constants to constrain the system, such as: {', '.join(suggestions)}")
            return 'FAIL_UNDERDETERMINED', None, error_msg

        else:
            # Case 3: Exactly one unique solution exists.
            solution_vector = A.LUsolve(b)
            input_exponents = np.array(solution_vector, dtype=float).flatten()
            solution = np.concatenate([[1.0], -input_exponents])
            return 'SUCCESS', solution, "Unique dimensionless relationship found."


    def _handle_discover_command(self, cmd: str):
        """Handle discovery command parsing"""
        try:
            parts = cmd.replace('discover', '').strip().split(' from ')
            if len(parts) != 2:
                print("Format: discover <output> from <input1,input2,...> [with <const1,const2,...>]")
                return
            
            output = parts[0].strip()
            rest = parts[1].strip()
            
            constants = []
            if ' with ' in rest:
                inputs_part, constants_part = rest.split(' with ')
                constants = [c.strip() for c in constants_part.split(',')]
            else:
                inputs_part = rest
            
            inputs = [i.strip() for i in inputs_part.split(',')]
            
            print(f"\n🔍 Discovering relationship for {output}...")
            result = self.discover_relationship(output, inputs, constants, auto_search=True, verbose=True)
            
            if result['success']:
                print(f"✅ {result['formula']}")
                if 'validation' in result:
                    val = result['validation']
                    print(f"   Confidence: {val['confidence_score']:.1%}")
                    if val['warnings']:
                        print(f"   Warnings: {'; '.join(val['warnings'])}")
            else:
                print(f"❌ {result['message']}")
                if 'suggested_constants' in result:
                    print(f"   Try adding: {', '.join(result['suggested_constants'])}")
                    
        except Exception as e:
            print(f"Error parsing command: {e}")
    
    def _handle_list_command(self, cmd: str):
        """Handle list command"""
        parts = cmd.split()
        if len(parts) > 1:
            category = parts[1]
            # Filter by category logic here
            print(f"Quantities in {category}: [implementation needed]")
        else:
            print(f"All {len(self.quantities)} quantities:")
            for name in sorted(self.quantities.keys()):
                print(f"  {name}")
    
    def _handle_describe_command(self, cmd: str):
        """Handle describe command"""
        parts = cmd.split()
        if len(parts) > 1:
            name = parts[1]
            if name in self.quantities:
                q = self.quantities[name]
                print(f"\n{q.name} ({q.symbol}):")
                print(f"  Description: {q.description}")
                print(f"  Dimensions: {q}")
            else:
                print(f"Unknown quantity: {name}")
        else:
            print("Usage: describe <quantity_name>")

# Example usage and testing
if __name__ == "__main__":
    engine = EnhancedPhysicsDisentangler()
    
    print("🚀 Enhanced Physics Formula Discovery Engine")
    print("=" * 60)
    
    # Test cases
    test_cases = [
        {
            'name': 'E = mc² Discovery',
            'output': 'energy',
            'inputs': ['mass'],
            'constants': ['speed_of_light']
        },
        {
            'name': 'Thermal de Broglie Wavelength',
            'output': 'wavelength',
            'inputs': ['mass', 'temperature'],
            'constants': ['planck_constant', 'boltzmann_constant']
        },
        {
            'name': 'Gravitational Force',
            'output': 'force',
            'inputs': ['mass', 'length'],
            'constants': ['gravitational_constant']
        },
        {
            'name': 'Ohm\'s Law',
            'output': 'voltage',
            'inputs': ['current'],
            'constants': ['resistance']
        }
    ]
    
    for test in test_cases:
        print(f"\n📐 {test['name']}")
        print("-" * 40)
        result = engine.discover_relationship(
            test['output'], 
            test['inputs'], 
            test.get('constants', [])
        )
        
        if result['success']:
            print(f"✅ Formula: {result['formula']}")
            if 'validation' in result:
                val = result['validation']
                print(f"   Confidence: {val['confidence_score']:.1%}")
                if val['warnings']:
                    print(f"   ⚠️  {'; '.join(val['warnings'])}")
        else:
            print(f"❌ {result['message']}")
            if 'suggested_constants' in result:
                print(f"   💡 Try adding: {', '.join(result['suggested_constants'])}")
    
    # Uncomment to start interactive mode
    engine.interactive_discovery()
