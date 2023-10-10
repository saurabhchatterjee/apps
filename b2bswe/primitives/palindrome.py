# https://backtobackswe.com/platform/content/check-if-a-number-is-a-palindrome
# A palindrome is a sequence that reads the same forwards and backward.
# Given an integer as input, write a function that tests if it is a palindrome.


class Solution:
    def isPalindrome(self, x):
        '''
        :type x: int
        :rtype: bool
        '''
        if x< 0:
            return False
        output = []
        while x:
            output.append(x%10)
            x = x//10
        n = len(output)
        for i in range(n//2):
            if output[i]!=output[n-1-i]:
                return False
        return True

# Solution is O(n) time. better solution was to use a mask to extract the most sinificant digit. 
# clever math, but the runtime is same. 

if __name__ == '__main__':
    nums = [12321, 9, 929, 9001, -121]
    for num in nums:
        print(f"{num}: {Solution().isPalindrome(num)}")
    
