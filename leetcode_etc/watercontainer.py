# Water container with largest volume
# Left bar moving right
# Right bar moving Left

def maxArea(height):
    l = 0
    r = len(height) - 1
    max_area = 0
    
    while l < r:
        l_h = height[l]
        r_h = height[r]
        
        cur_area = (r - l) * min(l_h, r_h)
        
        if cur_area > max_area:
            max_area = max(max_area, cur_area)
            
        if l_h > r_h:
            r -= 1
        else:
            l += 1
    
    return max_area

# Time complexity:      0(N)
# Space complexity:     0(1)

def main():
    print(maxArea([1,8,6,2,5,4,8,3,7]))

if __name__ == "__main__":
    main()