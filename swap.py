with open('index.html', 'r') as f:
    lines = f.readlines()

def find_bounds(start_id):
    start = -1
    end = -1
    for i, line in enumerate(lines):
        if f'id="{start_id}"' in line:
            start = i
            break
    if start != -1:
        for i in range(start, len(lines)):
            if '</section>' in lines[i]:
                end = i
                break
    return start, end

e_s, e_e = find_bounds('education')
p_s, p_e = find_bounds('public-presence')

if e_s != -1 and p_s != -1:
    # They should be contiguous or somewhat disjoint
    # E is first, P is second.
    ed_lines = lines[e_s:e_e+1]
    pub_lines = lines[p_s:p_e+1]
    
    # We reconstruct the file
    # Lines before E
    part1 = lines[:e_s]
    # Lines between E and P
    part2 = lines[e_e+1:p_s]
    # Lines after P
    part3 = lines[p_e+1:]
    
    new_lines = part1 + pub_lines + part2 + ed_lines + part3
    
    with open('index.html', 'w') as f:
        f.writelines(new_lines)
    print("Swapped!")
else:
    print("Not found")
