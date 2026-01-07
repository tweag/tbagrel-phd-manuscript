import sys
import re

PAT = "[^{ ]+|\{[^}]+\}"

def extract_radical(arg):
    if "{" in arg:
        return arg.strip()
    matches = re.findall(r"([A-Z][0-9']+)", arg)
    if len(matches) == 1:
        return matches[0]
    else:
        return None

def is_disjoint(dic, rad1, rad2):
    if (rad1, rad2) in dic:
        return (rad1, rad2), True
    if (rad2, rad1) in dic:
        return (rad2, rad1), True
    return None, False

def main():
    if len(sys.argv) != 3:
        print("Usage: python patch_rules.py <input_rule_file> <output_rule_file>")
        sys.exit(1)
    
    input_rule_file = sys.argv[1]
    output_rule_file = sys.argv[2]
    with open(input_rule_file, "r", encoding="utf-8") as f:
        rules = f.read()

    groups = [[l for l in group.split("\n") if l.strip()] for group in rules.split("\n\n") if group.strip()]

    output_groups = []
    for group in groups:
        output_group = []
        disjoints = dict()
        for l in group:
            if "DestOnly [[D" in l: continue
            if "UserDefined [[P" in l: continue
            if "ValidOnly [[" in l: continue
            if "IsValid" in l : continue
            match = re.search((r"\{\{ *\[\[(.*)\]\] *" + "#" + r" *\[\[(.*)\]\] *\}\}"), l)
            if match is not None:
                disjoints[(extract_radical(match.group(1)), extract_radical(match.group(2)))] = [l, False]
                continue
            match = re.search(r"(PAT) \+ (PAT) \+ (PAT)".replace("PAT", PAT), l)
            if match is not None:
                arg1 = extract_radical(match.group(1))
                arg2 = extract_radical(match.group(2))
                arg3 = extract_radical(match.group(3))

                (d1_key, is_dis1) = is_disjoint(disjoints, arg1, arg2)
                (d2_key, is_dis2) = is_disjoint(disjoints, arg1, arg3)
                (d3_key, is_dis3) = is_disjoint(disjoints, arg2, arg3)
                if (is_dis1 and is_dis2 and is_dis3):
                    output_group.append(re.sub(r"((?:PAT) \+ (?:PAT) \+ (?:PAT))".replace("PAT", PAT), f"{match.group(1)} , {match.group(2)} , {match.group(3)}", l))
                    disjoints[d1_key][1] = True
                    disjoints[d2_key][1] = True
                    disjoints[d3_key][1] = True
                    continue
            match = re.search(r"(PAT) \+ (PAT)".replace("PAT", PAT), l)
            if match is not None:
                arg1 = extract_radical(match.group(1))
                arg2 = extract_radical(match.group(2))
                (d1_key, is_dis1) = is_disjoint(disjoints, arg1, arg2)
                if is_dis1:
                    output_group.append(re.sub(r"((?:PAT) \+ (?:PAT))".replace("PAT", PAT), f"{match.group(1)} , {match.group(2)}", l))
                    disjoints[d1_key][1] = True
                    continue
            output_group.append(l)
            # space "2-3 chars mod" stimes Arg
            # space "3-4 chars in paren" stimes Arg
            # - args
            # Forbid DPG
        output_group = [ v[0] for k, v in disjoints.items() if not v[1] ] + output_group
        output_groups.append(output_group)

    with open(output_rule_file, "w", encoding="utf-8") as f:
        for group in output_groups:
            f.write("\n".join(group) + "\n\n")

if __name__ == "__main__":
    main()

