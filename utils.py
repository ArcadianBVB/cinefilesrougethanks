def compresser_nombres(liste_str):
    """
    Reçoit une chaîne de nombres séparés par des virgules, ex. "1,2,3,5,6,10",
    et renvoie une chaîne compressée, par exemple "1 à 3, 5 à 6, 10".
    """
    liste_str = liste_str.strip()
    if not liste_str:
        return ""
    nums = []
    for x in liste_str.split(","):
        x = x.strip()
        if x.isdigit():
            nums.append(int(x))
    if not nums:
        return ""
    nums = sorted(set(nums))
    result = []
    start = nums[0]
    end = start
    for n in nums[1:]:
        if n == end + 1:
            end = n
        else:
            if start == end:
                result.append(str(start))
            else:
                result.append(f"{start} à {end}")
            start = n
            end = n
    if start == end:
        result.append(str(start))
    else:
        result.append(f"{start} à {end}")
    return ", ".join(result)
