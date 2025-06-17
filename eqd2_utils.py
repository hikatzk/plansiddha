# eqd2_utils.py

def calc_eqd2(total_dose: float, num_fractions: int, alpha_beta: float) -> float:
    if num_fractions <= 0 or alpha_beta <= 0:
        raise ValueError("分割数とα/βは正の値にしてください")

    d = total_dose / num_fractions
    eqd2 = total_dose * ((d + alpha_beta) / (2 + alpha_beta))
    return round(eqd2, 2)