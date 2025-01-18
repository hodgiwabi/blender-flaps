import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Generate formulas for flap positions')
    parser.add_argument('num_flaps', type=int, help='Number of flaps to generate formulas for')
    return parser.parse_args()
def generate_flap_formula(position, total_flaps):
    """Generate the formula for a specific flap position"""

    # The main formula components
    part1 = f"pi-({position}*2)*pi/{total_flaps}+(({total_flaps}-2)/2)*(2*atan(tan(a/2-pi/2))+pi-({position}*2)*pi/{total_flaps}))"
    part2 = f"cos(a-(({position}-1)*2)/{total_flaps}*pi)>=0 and sin(a-(({position}-1)*2)/{total_flaps}*pi)<sin(-2*pi+2*pi/{total_flaps})and sin(a-(({position}-1)*2)/{total_flaps}*pi)>sin(-2*pi)"
    part3 = "-a"
    part4 = f"sin(a-(({position}-1)*2)/{total_flaps}*pi)<=0 and cos(a-(({position}-1)*2)/{total_flaps}*pi)<=1 and cos(a-(({position}-1)*2)/{total_flaps}*pi)>=cos(-pi+2*pi/{total_flaps})"
    part5 = f"pi-(2*{position})*pi/{total_flaps}"

    # Combine into final formula
    formula = f"({part1} if({part2})else({part3} if({part4})else {part5})"

    return formula

def print_all_flap_formulas(num_flaps):
    """Print formulas for all flap positions"""
    for i in range(1, num_flaps+1):
        formula = generate_flap_formula(i, num_flaps)
        print(f"\nFlap {i}: {formula}")

if __name__ == '__main__':
    args = parse_args()
    print_all_flap_formulas(args.num_flaps)
